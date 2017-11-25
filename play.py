from gomill import boards, ascii_boards, common
from keras.models import load_model
from parse_sgfs import board_to_nn
import numpy as np
from keras.utils import np_utils
import parse_sgfs
from main import board_loss
import keras.losses

model = load_model("model.h5", custom_objects={'board_loss': board_loss})
board = boards.Board(19)

def zero_illegal(board, weights):
    for x in range(19):
        for y in range(19):
            pos = board.get(x, y)

            if not pos is None:
                weights[0][x + 19 * y] = 0

moves = []
while True:
    print ascii_boards.render_board(board)
    m = raw_input("move: ")
    print m
    playerpos = common.move_from_vertex(m, 19)
    moves.append(playerpos)
    board.play(row=playerpos[0], col=playerpos[1], colour='b')

    y = model.predict(np.array([board_to_nn(board, 'w', moves)]))
    zero_illegal(board, y)
    print np.reshape(y[0], (19, 19))

    i = np.argmax(y[0])


    moves.append((i % 19, i // 19))
    board.play(row=i % 19, col=i // 19, colour='w')
