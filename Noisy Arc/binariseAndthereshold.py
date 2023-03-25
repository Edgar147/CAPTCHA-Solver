import os
import preprocessing
import segmenting
import time


if __name__ == "__main__":
    # The first step, binarization
    start = time.time()
    #Binarsation
    picturepath = os.listdir(r"samples/")
    for filelist in picturepath:
        open_path = "samples/" + filelist
        save_path = "preprocessing_data/image_binary/" + filelist[:-4]
        preprocessing.binary(open_path, save_path, "average_threshold")

    # Dilatation
    picturepath = os.listdir(r"preprocessing_data/image_binary")
    for filelist in picturepath:
        open_path = "preprocessing_data/image_binary/" + filelist
        save_path = "preprocessing_data/removelines/" + filelist+".png"
        preprocessing.dilation(open_path, save_path)


    #Erosion
    picture_path = os.listdir(r"preprocessing_data/removelines")
    for filelist in picture_path:
        open_path = "preprocessing_data/removelines/" + filelist
        save_path = "preprocessing_data/image_erosion/" + filelist
        preprocessing.erosion_line(open_path, save_path)


    # Segmentation verticale
    picturepath = os.listdir(r"preprocessing_data/image_erosion/")
    for filelist in picturepath:
        openpath = "preprocessing_data/image_erosion/" + filelist
        save_path = "preprocessing_data/segment/" + filelist[:-4]
        character = filelist.split(".")[0]
        segmenting.getVProjection(openpath, save_path, character, edge = 3, extend = 2)


    #Segmentation horizontale
    picturepath = os.listdir(r"preprocessing_data/segment/")
    for filelist in picturepath:
        open_path = "preprocessing_data/segment/" + filelist
        save_path = "preprocessing_data/segmentresult/" + filelist[:-4]
        segmenting.getHProjection(open_path, save_path, edge = 2)

    time = time.time() - start
    print("time:",time)