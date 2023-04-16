import os
import preprocessing
import segmenting
import time


if __name__ == "__main__":
    for i in range(1,21):
        exec(open('preprocessing_data/reset.py').read())
        print("Remise à zéro des données...")

        os.chdir("preprocessing_data")

        exec(open('binarize.py').read())
        print("Binarisation des données...")

        exec(open('supprimeBruitLignes.py').read())
        print("Supprimer les lignes...")

        exec(open('randSelect100.py').read())
        print("Récuperer 100 images pour les statistiques...")


        # # The first step, binarization
        # #Binarsation
        # picturepath = os.listdir(r"samples/")
        # for filelist in picturepath:
        #     open_path = "samples/" + filelist
        #     save_path = "preprocessing_data/image_binary/" + filelist[:-4]
        #     preprocessing.binary(open_path, save_path, "average_threshold")

        # Dilatation
        picturepath = os.listdir(r"image_binary")
        for filelist in picturepath:
            open_path = "image_binary/" + filelist
            save_path = "removelines/" + filelist+".png"
            preprocessing.dilation(open_path, save_path)


        #Erosion
        picture_path = os.listdir(r"removelines")
        for filelist in picture_path:
            open_path = "removelines/" + filelist
            save_path = "image_erosion/" + filelist
            preprocessing.erosion_line(open_path, save_path)


        # Segmentation verticale
        picturepath = os.listdir(r"image_erosion/")
        for filelist in picturepath:
            openpath = "image_erosion/" + filelist
            save_path = "segment/" + filelist[:-4]
            character = filelist.split(".")[0]
            segmenting.getVProjection(openpath, save_path, character, edge = 3, extend = 2)


        #Segmentation horizontale
        picturepath = os.listdir(r"segment/")
        for filelist in picturepath:
            open_path = "segment/" + filelist
            save_path = "segmentresult/" + filelist[:-4]
            segmenting.getHProjection(open_path, save_path, edge = 2)


        os.chdir('..')
        os.chdir('preprocessing_data')
        print("Creation des dossiers...")
        exec(open('folders.py').read())
        os.chdir('..')
        print("Cropping des lettres...")
        exec(open('crop.py').read())
        os.chdir('..')
        exec(open('removepng.py').read())
        print("Le pré-traitement est terminé! ")
        exec(open('train_model.py').read())
        print("L'entrainement est terminé! ")

        exec(open('statistiques.py').read())


