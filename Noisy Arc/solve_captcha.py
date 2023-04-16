from time import sleep
from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import segmenting
import os
import cv2
import pickle
import preprocessing_data.crop
from PIL import Image
from matplotlib import pyplot as plt


model_filename = "captcha_model.hdf5"
model_labels_filename = "model_labels.dat"
input_folder = "preprocessing_data/image_erosion"

with open(model_labels_filename, "rb") as f:
    lb = pickle.load(f)

model = load_model(model_filename)

def solve(image_file):
    predictions = []

    openpath = image_file
    save_path = "segmented_data/"
    character = image_file[-9:].split(".")[0]
    # print(openpath)
    # print(save_path)
    # print(character)
    segmenting.getVProjection(openpath, save_path, character, edge=3, extend=2,solve=True)
    for i in range(0, 5):
        segmenting.getHProjection(save_path+str(i)+".png",save_path+str(i),edge = 2)
        preprocessing_data.crop.cropImg(save_path+str(i)+".png")




        # Resize the image to 20x20 and convert to a numpy array
        # print(save_path+str(i)+".png")
        # print(save_path+str(i)+".png")
        # print(save_path+str(i)+".png")
        img=cv2.imread(save_path+str(i)+".png")
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        roi = resize_to_fit(image_gray, 20, 20)
        roi = np.expand_dims(roi, axis=2)
        roi = np.expand_dims(roi, axis=0)

        # Make a prediction on the cropped image using the trained model
        prediction = model.predict(roi,verbose=0)
        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

    captcha_text = "".join(predictions)
    # print(captcha_text)
    # print("effacer")
    folder_path = "segmented_data"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    return captcha_text





    #
    #
    #
    #
    # image = cv2.imread(image_file)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
    #
    # predictions = []
    # for ctr in contours:
    #     x, y, w, h = cv2.boundingRect(ctr)
    #     roi = gray[y:y+h, x:x+w]
    #     plt.imshow(roi)
    #     plt.show()
    #     # Check the percentage of filled pixels in the contour
    #     filled_pixels = cv2.countNonZero(roi)
    #     total_pixels = roi.shape[0] * roi.shape[1]
    #     filled_ratio = filled_pixels / float(total_pixels)
    #     if filled_ratio < 0.05:
    #         continue
    #
    #     # Resize the image to 20x20 and convert to a numpy array
    #     roi = resize_to_fit(roi, 20, 20)
    #     roi = np.expand_dims(roi, axis=2)
    #     roi = np.expand_dims(roi, axis=0)
    #
    #     # Make a prediction on the cropped image using the trained model
    #     prediction = model.predict(roi,verbose=0)
    #     letter = lb.inverse_transform(prediction)[0]
    #     predictions.append(letter)
    #
    # captcha_text = "".join(predictions)
    # return captcha_text
