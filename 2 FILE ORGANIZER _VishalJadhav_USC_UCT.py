import os
import shutil
import tkinter as tk
from tkinter import filedialog

def organize_files(directory):
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".doc", ".docx", ".txt", ".pdf"],
        "Videos": [".mp4", ".avi", ".mkv"],
        # Add more file types and corresponding folders as needed
    }

    # Create folders if they don't exist
    for folder in file_types.keys():
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Scan the directory and move files to the appropriate folders
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1]
            for folder, extensions in file_types.items():
                if file_ext.lower() in extensions:
                    destination_folder = os.path.join(directory, folder)
                    shutil.move(file_path, destination_folder)
                    break

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        organize_files(directory)
        print("Files organized successfully!")

# Create the main window
window = tk.Tk()
window.title("File Organizer")

# Create a button to select the directory
select_button = tk.Button(window, text="Select Directory", command=select_directory)
select_button.pack(pady=10)

# Run the GUI main loop
window.mainloop()