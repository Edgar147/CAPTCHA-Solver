import os
import shutil
from PIL import Image

def cropImg(file_path):
    # Load the image
    image = Image.open(file_path)

    minX = 0
    minXSave = 0
    maxXSave = 0

    # Récupérer la largeur et la hauteur de l'image
    largeur, hauteur = image.size

    nbPixelCaractere = 0
    nbPixelCaractereSave = 0
    pixelNoir = 0

    # Parcourir chaque pixel de l'image
    for x in range(largeur):
        for y in range(hauteur):
            # Récupérer la valeur du pixel à la position (x,y)
            pixel = image.getpixel((x,y))
            if pixel == 0:
                pixelNoir = pixelNoir + 1
                maxX = x

        if pixelNoir == 0 or (x == largeur-1 and y == hauteur-1):
            if (nbPixelCaractere > nbPixelCaractereSave):
                maxXSave = x
                minXSave = minX
                nbPixelCaractereSave = nbPixelCaractere

            nbPixelCaractere = 0
        else:
            if nbPixelCaractere == 0:
                minX = x
            nbPixelCaractere = nbPixelCaractere + pixelNoir
        pixelNoir = 0

    cropped_img = image.crop((minXSave, 0, maxXSave, hauteur))

    # Enregistrer l'image recadrée dans le dossier output_dir
    filename = os.path.splitext(os.path.basename(file_path))[0]
    cropped_img.save(file_path)

if __name__ == '__main__':
    input_dir = "letter"

    # Parcourir tous les dossiers dans le dossier d'entrée
    for folder_name in os.listdir(input_dir):
        # Vérifier si le nom de dossier contient une lettre ou un chiffre
        if any(char.isalnum() for char in folder_name) and folder_name != 'm':

            # Parcourir tous les fichiers dans le dossier de lettre/chiffre
            for filename in os.listdir(os.path.join(input_dir, folder_name)):
                # Vérifier si le fichier est une image PNG
                if filename.endswith(".png"):
                    #print(filename)
                    # Appeler la fonction cropImg pour recadrer l'image
                    file_path = os.path.join(input_dir, folder_name, filename)
                    cropImg(file_path)




    # Define the paths to the source and target folders
    cwd = os.getcwd()
    source_folder = 'letter'
    target_folder = '../letter'

    if os.path.exists(target_folder):
        # If the target directory exists, delete it and its contents
        shutil.rmtree(target_folder)
    shutil.move(source_folder, target_folder)


    # Move the source folder into the target folder
    #os.rename(source_folder, os.path.join(target_folder, source_folder))
