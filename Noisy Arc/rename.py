import os

# Change the working directory to the folder containing the files
os.chdir('samples')

# Loop through each file in the directory
for filename in os.listdir('.'):
    # Check if the filename contains an underscore
    if '_' in filename:
        # Split the filename into the prefix and the rest of the name
        prefix, rest = filename.split('_', 1)

        # Rename the file with just the rest of the name
        os.rename(filename, rest)
