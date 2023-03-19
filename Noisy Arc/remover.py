import os

# List all files in a specific directory
directory = os.getcwd()
directory +="/samples"
files = os.listdir(directory)

# Loop through the files and delete PNG files
for file in files:
    if file.endswith(".png"):
        os.remove(os.path.join(directory, file))
