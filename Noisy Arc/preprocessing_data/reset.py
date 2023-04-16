import os
import shutil

# Loop through all items in the current working directory
for item in os.listdir():
    # Check if the item is a directory
    if os.path.isdir(item):
        # Loop through all items in the directory
        for subitem in os.listdir(item):
            # Create the full path to the item
            subitem_path = os.path.join(item, subitem)
            # Check if the subitem is a file, and skip it
            if os.path.isfile(subitem_path):
                continue
            # If the subitem is a directory, delete its contents recursively
            elif os.path.isdir(subitem_path):
                for subsubitem in os.listdir(subitem_path):
                    subsubitem_path = os.path.join(subitem_path, subsubitem)
                    if os.path.isfile(subsubitem_path):
                        os.remove(subsubitem_path)
                    elif os.path.isdir(subsubitem_path):
                        shutil.rmtree(subsubitem_path)
