from gomill import boards

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Convolution2D, MaxPooling2D, Add, Input, ZeroPadding2D
from keras.utils import np_utils
from keras.models import Model
from keras.models import load_model
from parse_sgfs import parse_all
from keras.datasets import mnist
from keras import backend

from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

TESTING_SIZE = 1000
NUM_FEAT_PLANES = 4


def main():

    (x_train, y_train) = parse_all()
    x_train = np.array(x_train)
    x_train = x_train.reshape(x_train.shape[0], 19, 19, NUM_FEAT_PLANES)

    y_train = [x + y * 19 for x, y in y_train]
    y_train = np_utils.to_categorical(y_train, 361)
    y_train = y_train.astype('float32')

    x_test = x_train[-TESTING_SIZE:]
    x_train = x_train[:-TESTING_SIZE]
    y_test = y_train[-TESTING_SIZE:]
    y_train = y_train[:-TESTING_SIZE]

    print "Training on", len(x_train), "positions"

    #model = load_model('model.h5')
    model = res_net()
    model.compile(loss='binary_cross_entropy',
                  optimizer='adam', metrics=['mean_squared_error'])
    model.fit(x_train, y_train, batch_size=1024, epochs=2, verbose=1)

    score = model.evaluate(x_test, y_test, verbose=1)
    print "Testing score: ", score
    model.save('model.h5')


def convolutional_block(l):
    l = Convolution2D(128, (3, 3), activation='leakyrelu', padding="same")(l)
    l = BatchNormalization()(l)
    return l


def residual_block(l):
    m = Convolution2D(128, (3, 3), activation='leakyrelu', padding="same")(l)
    m = BatchNormalization()(m)
    m = Convolution2D(128, (3, 3), activation='leakyrelu', padding="same")(m)
    m = BatchNormalization()(m)

    l = Add()([l, m])
    return l


def res_net():
    inp = Input(shape=(19, 19, NUM_FEAT_PLANES))
    l = convolutional_block(inp)

    for i in range(3):
        l = residual_block(l)

    l = Flatten()(l)
    output = Dense(361, activation='sigmoid')(l)

    model = Model(inputs=inp, outputs=output)
    return model


def conv_net():
    model = Sequential()
    model.add(Convolution2D(256, (3, 3), activation='relu',
                            input_shape=(19, 19, NUM_FEAT_PLANES), padding="same"))
    model.add(BatchNormalization())
    model.add(Convolution2D(256, (3, 3), activation='relu',
                            input_shape=(19, 19, NUM_FEAT_PLANES), padding="same"))
    model.add(BatchNormalization())
    model.add(Convolution2D(256, (3, 3), activation='relu',
                            input_shape=(19, 19, NUM_FEAT_PLANES), padding="same"))
    model.add(Flatten())
    model.add(Dense(361, activation='softmax'))

    return model


def board_loss(y_true, y_pred):
    inv_true = 1 - y_true
    reduc = y_pred - inv_true
    reduc = backend.clip(reduc, -0.1, None)
    reduc **= 2
    return 1 - backend.mean(reduc, axis=-1)


if __name__ == "__main__":
    main()
