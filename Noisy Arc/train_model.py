import pickle

import cv2
import os.path
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from helpers import resize_to_fit

# Set the input folder and output model paths
input_folder = "letter"
model_filename = "captcha_model.hdf5"
model_labels_filename = "model_labels.dat"
if os.path.exists(model_filename):
    os.remove(model_filename)
if os.path.exists(model_labels_filename):
    os.remove(model_labels_filename)
# Initialize the data and labels lists
data = []
labels = []

# Loop through the image files in the input folder
for image_file in paths.list_images(input_folder):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize the image to 20x20
    image = resize_to_fit(image, 20, 20)
    # Add a channel dimension to the image
    image = np.expand_dims(image, axis=2)
    # Extract the label from the image filename
    label = image_file.split(os.path.sep)[-2]
    # Add the image and label to the data and labels lists
    data.append(image)
    labels.append(label)

# Convert the data and labels lists to NumPy arrays
data = np.array(data, dtype="float32") / 255.0
labels = np.array(labels)

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(data, labels, test_size=0.25, random_state=0)

# Convert the labels from strings to binary vectors
lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# Save the label binarizer to disk
with open(model_labels_filename, "wb") as f:
    pickle.dump(lb, f)

# Build the model architecture
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(20, 20, 1)))
model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(19, activation='softmax'))


# Define optimizer, loss function and metrics
optimizer = Adam(learning_rate=0.001)
loss = "categorical_crossentropy"
metrics = ["accuracy"]

# Compile the model
model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

# Define training callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights= True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.15, patience=3)
history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=32, epochs=40,
callbacks=[early_stop, reduce_lr])
model.save(model_filename)


