from gomill import boards

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Convolution2D, MaxPooling2D, Add, Input, ZeroPadding2D
from keras.utils import np_utils
from keras.models import Model
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
y_train = y_train.astype('float32')


x_test = x_train[-200:]
x_train = x_train[:-200]
y_test = y_train[-200:]
y_train = y_train[:-200]

print "Training on", len(x_train), "positions"


def convolutional_block(l):
    l = Convolution2D(256, (3, 3), activation='relu',
                      input_shape=(19, 19, 2), padding="same")(l)
    l = BatchNormalization()(l)
    return l


def residual_block(l):
    m = Convolution2D(256, (3, 3), activation='relu',
                      input_shape=(19, 19, 2), padding="same")(l)
    m = BatchNormalization()(m)
    m = Convolution2D(256, (3, 3), activation='relu',
                      input_shape=(19, 19, 2), padding="same")(m)
    m = BatchNormalization()(m)
    l = Add()([l, m])
    return l


inp = Input(shape=(19, 19, 2))
l = convolutional_block(inp)

for i in range(5):
    l = residual_block(l)


l = Flatten()(l)
output = Dense(361, activation='relu')(l)

model = Model(inputs=inp, outputs=output)
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=512, epochs=10, verbose=1)
score = model.evaluate(x_test, y_test, verbose=1)
print "Training score: ", score
model.save('model.h5')
