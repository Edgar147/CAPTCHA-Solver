import os
import shutil

# Create a directory called 'basic_letter' if it doesn't exist
if not os.path.exists('letter'):
    os.makedirs('letter')

# Change the working directory to 'basic_letter'
os.chdir('letter')

# Create a list of all image files in the 'segmentresult' directory
image_files = [file for file in os.listdir('../segmentresult') if file.endswith('.png')]

# Loop through each image file
for order, image_file in enumerate(image_files, start=1):
    # Get the last character of the file name (before the file extension)
    character = os.path.splitext(image_file)[0][-1]

    # Create a directory with the name of the character (if it doesn't already exist)
    if not os.path.exists(character):
        os.makedirs(character)

    # Copy the image file to the character directory with the name of the order
    order_str = str(order).zfill(3)
    new_filename = f"{order_str}.png"
    shutil.copy(os.path.join('../segmentresult', image_file), os.path.join(character, new_filename))

