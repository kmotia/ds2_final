import os

# Define the folder name
folder_name = 'BSEMAN_files'

# Get a list of all files in the folder
file_list = os.listdir(folder_name)

# Iterate through each file in the folder
for filename in file_list:
    # Construct the new file name
    new_filename = filename[:1] + 'C' + filename[2:]
    
    # Construct the paths to the old and new files
    old_path = os.path.join(folder_name, filename)
    new_path = os.path.join(folder_name, new_filename)
    
    # Rename the file
    os.rename(old_path, new_path)
    print(f"File '{filename}' renamed to '{new_filename}'.")

print("All files renamed successfully.")
