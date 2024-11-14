import os

# Define the main directory path containing the folders to rename
directory_path = "images"

try:
    # Get a sorted list of folders only within the main directory
    folders = sorted([f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))])
except FileNotFoundError:
    print("The specified path does not exist. Please check the directory path.")
    folders = []

# Counter for sequential naming of folders
counter = 1

# Ensure the directory path doesn't end with a slash (optional to avoid path issues)
directory_path = directory_path.rstrip('/\\')

# Loop through each folder and assign a new name sequentially
for folder_name in folders:
    old_folder_path = os.path.join(directory_path, folder_name)
    
    # Check if the folder name starts with 'dog' and is followed by a number (e.g., dog1, dog2, dog3, ...)
    if folder_name.lower().startswith('dog') and folder_name[3:].isdigit():
        print(f"Skipping renaming for '{folder_name}' as it already follows the 'dog<number>' pattern.")
        continue
    
    # Generate the new folder name as "dog1", "dog2", "dog3", ...
    new_folder_name = f"dog{counter}"
    new_folder_path = os.path.join(directory_path, new_folder_name)
    
    # Check if the new folder name already exists and increment the number until a unique name is found
    while os.path.exists(new_folder_path):
        counter += 1
        new_folder_name = f"dog{counter}"
        new_folder_path = os.path.join(directory_path, new_folder_name)
    
    try:
        # Rename the folder to the new unique name
        os.rename(old_folder_path, new_folder_path)
        print(f"Folder '{os.path.basename(old_folder_path)}' has been renamed to '{os.path.basename(new_folder_path)}'")
        counter += 1  # Increase the counter for the next folder
        
        # Rename images inside the folder with sequential numbering
        image_counter = 1
        for filename in os.listdir(new_folder_path):
            file_path = os.path.join(new_folder_path, filename)
            
            if os.path.isfile(file_path):
                # Extract the file extension
                file_extension = os.path.splitext(filename)[1]
                
                # Define the new name for the image
                new_image_name = f"{image_counter}{file_extension}"
                new_image_path = os.path.join(new_folder_path, new_image_name)
                
                # Rename the image file
                os.rename(file_path, new_image_path)
                print(f"Renamed '{filename}' to '{new_image_name}'")
                image_counter += 1  # Increment image counter
        
    except PermissionError:
        print(f"Could not rename the folder '{os.path.basename(old_folder_path)}'. There may be a permissions issue.")

print("Renaming process completed.")
