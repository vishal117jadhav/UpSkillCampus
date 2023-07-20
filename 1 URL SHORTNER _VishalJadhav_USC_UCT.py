from flask import Flask, render_template, redirect, request
import string
import random
import sqlite3
import threading

# Create a thread-local storage for the database connection
local = threading.local()

app = Flask(__name__)

def get_database_connection():
    # Check if the current thread has a database connection
    if not hasattr(local, 'connection'):
        # If not, create a new connection
        local.connection = sqlite3.connect('url_shortener.db')
    return local.connection

def get_database_cursor():
    # Get the database connection for the current thread
    connection = get_database_connection()
    # Check if the current thread has a database cursor
    if not hasattr(local, 'cursor'):
        # If not, create a new cursor
        local.cursor = connection.cursor()
    return local.cursor

def close_database_connection(exception=None):
    # Close the database cursor (if exists)
    if hasattr(local, 'cursor'):
        local.cursor.close()
    # Close the database connection (if exists)
    if hasattr(local, 'connection'):
        local.connection.close()

@app.before_request
def before_request():
    # Create the database connection and cursor for the current thread
    get_database_connection()
    get_database_cursor()

@app.teardown_request
def teardown_request(exception=None):
    # Close the database connection and cursor after the request is completed
    close_database_connection(exception)

# Create the URL mapping table if it doesn't exist
def create_url_mapping_table():
    cursor = get_database_cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS url_mapping
                      (short_url TEXT PRIMARY KEY, long_url TEXT)''')
    cursor.connection.commit()

def generate_shortened_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_shortened_url()
        cursor = get_database_cursor()
        cursor.execute("INSERT INTO url_mapping VALUES (?, ?)", (short_url, long_url))
        cursor.connection.commit()
        return redirect('/')
    cursor = get_database_cursor()
    cursor.execute("SELECT * FROM url_mapping")
    url_mapping = cursor.fetchall()
    return render_template('index.html', url_mapping=url_mapping)

@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    cursor = get_database_cursor()
    cursor.execute("SELECT long_url FROM url_mapping WHERE short_url = ?", (short_url,))
    result = cursor.fetchone()
    if result:
        long_url = result[0]
        return redirect(long_url)
    return 'Invalid URL'

if __name__ == '__main__':
    create_url_mapping_table()
    app.run(debug=True)
