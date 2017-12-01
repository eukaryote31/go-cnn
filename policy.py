from gomill import boards
from parse_sgfs import board_to_nn
from keras.models import load_model


class NNPolicy:

    def __init__(modelfile, board_loss=None):
        model = load_model(modelfile, custom_objects={'board_loss': board_loss})

    def evaluate(self, board, currmove, moves):
        weights = self.model.predict(np.array([board_to_nn(board, 'w', moves)]))
        return zero_illegal(board, weights)


def zero_illegal(board, weights):
    for x in range(19):
        for y in range(19):
            pos = board.get(x, y)

            if not pos is None:
                weights[0][x + 19 * y] = 0
    return weights
