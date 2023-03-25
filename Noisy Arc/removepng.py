import os

folder_path = "preprocessing_data/image_erosion"

for file_name in os.listdir(folder_path):
    if file_name.endswith(".png"):
        new_file_name = file_name[:-4] # remove the last 4 characters (.png)
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_file_name)
        os.rename(old_path, new_path)
