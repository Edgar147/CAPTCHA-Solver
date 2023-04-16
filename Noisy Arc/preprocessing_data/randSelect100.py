import os
import random
import shutil

# Set the source and destination folders
src_folder = "image_binary"
dst_folder = "stats"

# Create the destination folder if it doesn't exist
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

# Get a list of all the files in the source folder
file_list = os.listdir(src_folder)

# Select 100 random files from the file list
selected_files = random.sample(file_list, 100)

# Move the selected files to the destination folder
for file_name in selected_files:
    src_path = os.path.join(src_folder, file_name)
    dst_path = os.path.join(dst_folder, file_name)
    shutil.move(src_path, dst_path)
    
print("100 files moved to 'stats' folder.")
