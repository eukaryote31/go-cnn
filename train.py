from gomill import boards

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from keras.layers import Convolution2D, MaxPooling2D, Add, Input, ZeroPadding2D, LeakyReLU
from keras.utils import np_utils
from keras.models import Model
from keras.models import load_model
from parse_sgfs import parse_all
from keras.datasets import mnist
from keras import backend
from keras import optimizers

from keras import backend as K

import cPickle as pickle

import numpy as np

TESTING_SIZE = 1000
NUM_FEAT_PLANES = 5
NUM_EPOCHS = 1
NUM_CONV_FILTERS = 256
BATCH_SIZE = 512
NUM_RES_BLOCKS = 4
TRAIN_EXISTING = True


def main():
    print "Loading data"
    with open("dataset.pickle", "rb") as fh:
        (x_train, y_train) = pickle.load(fh)
    print "Data loaded"

    x_train = np.array(x_train)
    x_train = x_train.reshape(x_train.shape[0], 19, 19, NUM_FEAT_PLANES)

    x_train = np.flip(x_train, axis=1)
    y_train = [(18 - x) + y * 19 for x, y in y_train]
    y_train = np_utils.to_categorical(y_train, 361)
    y_train = y_train.astype('float32')

    x_test = x_train[-TESTING_SIZE:]
    x_train = x_train[:-TESTING_SIZE]
    y_test = y_train[-TESTING_SIZE:]
    y_train = y_train[:-TESTING_SIZE]


    if TRAIN_EXISTING:
        model = load_model('model.h5')
    else:
        model = res_net()
        model.compile(loss="categorical_crossentropy",
                      optimizer=optimizers.Adam(), metrics=['accuracy'])

    print "Training on", len(x_train), "positions"
    model.fit(x_train, y_train, batch_size=BATCH_SIZE,
              epochs=NUM_EPOCHS, verbose=1)

    score = model.evaluate(x_test, y_test, verbose=1)
    print "Testing score: ", score
    model.save('model.h5')


def convolutional_block(l):
    l = Convolution2D(NUM_CONV_FILTERS, (3, 3), padding="same")(l)
    l = BatchNormalization()(l)
    l = LeakyReLU()(l)
    return l


def residual_block(l):
    m = Convolution2D(NUM_CONV_FILTERS, (3, 3), padding="same")(l)
    m = BatchNormalization()(m)
    m = LeakyReLU()(m)

    m = Convolution2D(NUM_CONV_FILTERS, (3, 3), padding="same")(m)
    m = BatchNormalization()(m)

    l = Add()([l, m])
    l = LeakyReLU()(l)
    return l


def board_loss():
    # todo
    pass


def res_net():
    """
    Network with architecture similar to AlpaGo Zero tower
    """
    inp = Input(shape=(19, 19, NUM_FEAT_PLANES))
    l = convolutional_block(inp)

    for i in range(NUM_RES_BLOCKS):
        l = residual_block(l)

    l = Convolution2D(2, (1, 1), padding="same")(l)
    l = BatchNormalization()(l)
    l = LeakyReLU()(l)

    l = Flatten()(l)
    l = Dense(361)(l)
    output = Activation('softmax')(l)

    model = Model(inputs=[inp], outputs=output)
    return model


def conv_net():
    """
    Network with similar architecture to the original AlphaGo policy net
    """
    model = Sequential()
    model.add(Convolution2D(NUM_CONV_FILTERS, (5, 5), activation='relu',
                            input_shape=(19, 19, NUM_FEAT_PLANES), padding="same"))
    for i in range(8):
        model.add(Convolution2D(NUM_CONV_FILTERS, (3, 3), activation='relu',
                                input_shape=(19, 19, NUM_FEAT_PLANES), padding="same"))
    model.add(Flatten())
    model.add(Dense(361, activation='softmax'))

    return model


def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))


if __name__ == "__main__":
    main()
