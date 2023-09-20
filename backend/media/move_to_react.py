import os
import shutil

# Get the current directory
current_directory = os.getcwd()

# Define the destination directory
destination_directory = os.path.join('..', 'mikeshop-react', 'mikeshop-react', 'public', 'media')

# List all folders in the current directory
folders_to_copy = [folder for folder in os.listdir(current_directory) if os.path.isdir(folder)]

for folder_name in folders_to_copy:
    source_folder_path = os.path.join(current_directory, folder_name)
    destination_folder_path = os.path.join(destination_directory, folder_name)

    # Check if the destination folder already exists
    if os.path.exists(destination_folder_path):
        print(f"Folder '{folder_name}' already exists in the destination directory.")
    else:
        # Copy the folder to the destination directory
        shutil.copytree(source_folder_path, destination_folder_path)
        print(f"Folder '{folder_name}' copied to the destination directory.")
