
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv1D, MaxPooling1D, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard
import numpy as np
import pickle
import time
from sklearn.utils import shuffle as skshuffle
import math

SPLIT = 0.8

heartbeats = np.load("../../compressedDataFull\heartbeats_f1.npy")
labels = np.load("../../compressedDataFull\labels_f1.npy")

heartbeats = np.asarray(heartbeats)
labels = np.asarray(labels)

shuffled_heartbeats, shuffled_labels = skshuffle(heartbeats, labels)

print(np.shape(shuffled_heartbeats))
print(np.shape(shuffled_labels))


NAME = "full-cnn-3-{}".format(int(time.time()))
tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

model = tf.keras.models.Sequential()

model.add(Conv1D(filters=(32), kernel_size=3, activation=tf.nn.relu, input_shape=(450, 2)))

model.add(Conv1D(filters=(64), kernel_size=3, activation=tf.nn.relu))
model.add(Conv1D(filters=(64), kernel_size=3, activation=tf.nn.relu))
model.add(Dropout(0.25))
model.add(MaxPooling1D(2, data_format='channels_last'))

model.add(Conv1D(filters=256, kernel_size=3, activation=tf.nn.relu))
model.add(Conv1D(filters=256, kernel_size=3, activation=tf.nn.relu))
model.add(Dropout(0.25))
model.add(MaxPooling1D(2, data_format='channels_last'))
model.add(Flatten())
model.add(Dense(1024, activation=tf.nn.relu))
model.add(Dense(20, activation=tf.nn.sigmoid))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) 

model.fit(shuffled_heartbeats, shuffled_labels, validation_split=0.3, epochs=10, callbacks=[tensorboard])