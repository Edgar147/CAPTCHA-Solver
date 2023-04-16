import os
from PIL import Image

import os

def remove_small_images(folder_path, min_size):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if not file_path.endswith('.png'):
                continue
            try:
                width, height = Image.open(file_path).size
                if width <= min_size or height <= min_size:
                    os.remove(file_path)
                    print("Removed:", file_path)
            except IOError as e:
                print(f"Could not open {file_path}: {e}")


# Example usage: remove images with width or height less than 100 pixels in folder 'my_folder'
remove_small_images("letter", 11)
