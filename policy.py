from gomill import boards
from parse_sgfs import board_to_nn
from keras.models import load_model
import numpy as np

class NNPolicy:

    def __init__(self, modelfile, board_loss=None):
        self.model = load_model(modelfile, custom_objects={'board_loss': board_loss})

    def evaluate(self, board, color, moves):
        weights = self.model.predict(np.array([board_to_nn(board, color, moves)]))
        return zero_illegal(board, weights, color)


def zero_illegal(board, weights, color):
    for x in range(19):
        for y in range(19):
            pos = board.get(x, y)


            if not pos is None:
                weights[0][x + 19 * y] = 0
            else:
                # suicide rule
                boardcopy = board.copy()
                boardcopy.play(x, y, color)
                if boardcopy.get(x, y) is None:
                    weights[0][x + 19 * y] = 0
    return weights
