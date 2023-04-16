import cv2
import os


# Define the relative path to the 'samples' folder
samples_path = os.path.abspath(os.path.join(os.getcwd(), '../samples'))

# Create the 'bins' folder if it doesn't exist
if not os.path.exists('binaire_start'):
    os.makedirs('binaire_start')

# Loop through all files in the 'samples' folder
for filename in os.listdir(samples_path):
    # Load the image in grayscale mode
    img = cv2.imread(os.path.join(samples_path, filename), cv2.IMREAD_GRAYSCALE)

    # Apply adaptive thresholding to binarize the image
    threshold_value = 127
    max_value = 255
    _, thresh = cv2.threshold(img, threshold_value, max_value, cv2.THRESH_BINARY)

    # Save the binarized image in the 'bins' folder
    cv2.imwrite(os.path.join('binaire_start', filename), thresh)

    # Display the binarized image
    # cv2.imshow('Binarized Image', thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
