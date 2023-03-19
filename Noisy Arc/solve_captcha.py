from time import sleep
from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import imutils
import cv2
import pickle
from PIL import Image
from matplotlib import pyplot as plt


model_filename = "C:\\Users\\karap\\Desktop\\M1\\IR\\CAPTCHA-Solver-master\\Noisy Arc\\captcha_model.hdf5"
model_labels_filename = "C:\\Users\\karap\\Desktop\\M1\\IR\\CAPTCHA-Solver-master\\Noisy Arc\\model_labels.dat"
input_folder = "C:\\Users\\karap\\Desktop\\M1\\IR\\CAPTCHA-Solver-master\\Noisy Arc\\samples"

with open(model_labels_filename, "rb") as f:
    lb = pickle.load(f)

model = load_model(model_filename)

def solve(image_file):
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    predictions = []
    for ctr in contours:
        x, y, w, h = cv2.boundingRect(ctr)
        roi = gray[y:y+h, x:x+w]

        # Resize the image to 20x20 and convert to a numpy array
        roi = resize_to_fit(roi, 20, 20)
        roi = np.expand_dims(roi, axis=2)
        roi = np.expand_dims(roi, axis=0)

        # Make a prediction on the cropped image using the trained model
        prediction = model.predict(roi)
        letter = lb.inverse_transform(prediction)[0]
        predictions.append(letter)

    captcha_text = "".join(predictions)
    return captcha_text
