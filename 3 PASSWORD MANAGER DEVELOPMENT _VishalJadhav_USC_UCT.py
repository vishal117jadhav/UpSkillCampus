import sqlite3
import bcrypt
from cryptography.fernet import Fernet
from getpass import getpass
import string
import random

# Connect to the database
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account TEXT,
        username TEXT,
        password TEXT
    )
''')

# Generate a key for encrypting and decrypting passwords
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())


def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()


def save_password(account, username, password):
    encrypted_password = encrypt_password(password)
    c.execute("INSERT INTO passwords (account, username, password) VALUES (?, ?, ?)",
              (account, username, encrypted_password))
    conn.commit()


def retrieve_password(account):
    c.execute("SELECT username, password FROM passwords WHERE account=?", (account,))
    result = c.fetchone()
    if result:
        username, encrypted_password = result
        password = decrypt_password(encrypted_password)
        return username, password
    else:
        return None


def generate_and_save_password(account, username):
    password = generate_password()
    save_password(account, username, password)
    return password


def main_menu():
    print("Password Manager")
    print("1. Add a password")
    print("2. Retrieve a password")
    print("3. Generate and save a password")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        account = input("Enter account name: ")
        username = input("Enter username: ")
        password = getpass("Enter password: ")
        save_password(account, username, password)
        print("Password saved successfully.\n")
    elif choice == "2":
        account = input("Enter account name: ")
        result = retrieve_password(account)
        if result:
            username, password = result
            print("Username:", username)
            print("Password:", password)
        else:
            print("No password found for the account.\n")
    elif choice == "3":
        account = input("Enter account name: ")
        username = input("Enter username: ")
        password = generate_and_save_password(account, username)
        print("Generated password:", password)
    elif choice == "4":
        exit()
    else:
        print("Invalid choice.\n")

    main_menu()


if __name__ == "__main__":
    main_menu()