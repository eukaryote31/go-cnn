from gomill import boards

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Convolution2D, MaxPooling2D, merge
from keras.utils import np_utils
from parse_sgfs import parse_all

from keras.datasets import mnist

from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

(x_train, y_train) = parse_all()
x_train = np.array(x_train)
x_train = x_train.reshape(x_train.shape[0], 19, 19, 2)

y_train = [x + y * 19 for x, y in y_train]
y_train = np_utils.to_categorical(y_train, 361)



print "Training on", len(x_train), "positions"

model = Sequential()


def convolutional_block(model):
    model.add(Convolution2D(
        256, (3, 3), activation='relu', input_shape=(19, 19, 2)))
    model.add(BatchNormalization())


def residual_block(model):
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(merge.add())


convolutional_block(model)

residual_block(model)
residual_block(model)
residual_block(model)

model.add(Flatten())
model.add(Dense(361, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=512, epochs=10, verbose=1)
score = model.evaluate(x_test, y_test, verbose=1)
 print "Training score: ", score
model.save('model.h5')
