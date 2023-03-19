from random import choices
from string import ascii_lowercase, digits
from PIL import Image, ImageDraw, ImageFont

width, height = 200, 50
font_size = 40
font = ImageFont.truetype("arial.ttf", font_size)

exec(open('remover.py').read())

# Define the characters to exclude from the random string
exclude_digits = '019'
exclude_letters = 'ahijkolqrstuvz'

for i in range(1000):
    # Generate a random 5-character alphanumeric string
    random_digits = ''.join([d for d in digits if d not in exclude_digits])
    random_letters = ''.join([l for l in ascii_lowercase if l not in exclude_letters])
    random_string = ''.join(choices(random_digits + random_letters, k=5))

    # Create a new image with a grey gradient background
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for x in range(width):
        grey_value = int((x / width) ** 2 * 152)+255
        draw.line((x, 0, x, height), fill=(grey_value, grey_value, grey_value))

    # Draw the random string on the image
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(random_string, font=font)
    draw.text(((width - text_width) / 2, (height - text_height) / 2), random_string, font=font, fill="black")
    random_string = str(i)+"_"+random_string
    # Save the image as a PNG file with a name based on the random string
    image.save(f"samples/{random_string}.png")
