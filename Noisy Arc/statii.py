import os
import matplotlib.pyplot as plt
from solve_captcha import solve

# Set the path to the directory containing the images
image_dir = "preprocessing_data/image_erosion"
correct_count = 0
incorrect_count = 0

# Define the list of characters to exclude from statistics
exclude_chars = 'ahijkolqrstuvz019'

# Create a list of characters to keep track of
correct_counts = {char: 0 for char in "2345678bcdefgmnpwxy"}
incorrect_counts = {char: 0 for char in "2345678bcdefgmnpwxy"}

# Loop through all images in the directory
for image_file in os.listdir(image_dir):
    # Get the full path to the image file
    image_path = os.path.join(image_dir, image_file)

    # Solve the captcha using the solve function
    predicted_text = solve(image_path)

    # Get the filename without the extension
    filename = os.path.splitext(image_file)[0]

    # Check if the predicted text matches the filename
    if predicted_text == filename:
        print(f"Prediction pour {image_file}: {predicted_text} (CORRECT)")
        correct_count += 1
    else:
        print(f"Prediction pour {image_file}: {predicted_text} (INCORRECT)")
        incorrect_count += 1

    # Update the character statistics
    for pred_char, true_char in zip(predicted_text, filename):
        if pred_char == true_char:
            correct_counts[true_char] += 1
        else:
            incorrect_counts[true_char] += 1

total_count = correct_count + incorrect_count
accuracy = correct_count / total_count
print("Precision totale: {:.2f}%".format(accuracy * 100))

# Create a list of tuples containing each character and its accuracy
char_accuracy = []
for char in "2345678bcdefgmnpwxy":
    total_count = correct_counts[char] + incorrect_counts[char]
    if total_count > 0:
        accuracy = correct_counts[char] / total_count
        char_accuracy.append((char, accuracy))
    else:
        char_accuracy.append((char, 0))

# Sort the list based on the accuracy in descending order
char_accuracy = sorted(char_accuracy, key=lambda x: x[1], reverse=False)

# Print the results for each character, sorted by accuracy
for char, accuracy in char_accuracy:
    total_count=correct_counts[char] + incorrect_counts[char]
    print("{}: precision={:.2f}% ({}/{} Nombre de prédictions erronées à cause de ce caractère {})".format(char, accuracy * 100, correct_counts[char], total_count,total_count-correct_counts[char]))

# Print the total number of correct and incorrect predictions
print("Predictions correctes: {}".format(correct_count))
print("Predictions incorrectes: {}".format(incorrect_count))
print("Correcte -> {:.2f}%".format((correct_count/1000)*100))
print("Incorrecte -> {:.2f}%".format((incorrect_count/1000)*100))

# Create a bar plot of the accuracy rate for each character
fig, ax = plt.subplots()
ax.bar([x[0] for x in char_accuracy], [x[1] for x in char_accuracy])
ax.set_xlabel("Caractère")
ax.set_ylabel("Taux de Precision")
ax.set_title("Taux de Precision pour chaque caractère")
#Il faut verifier le % des incorrects produits par n/m et 7
plt.show()
