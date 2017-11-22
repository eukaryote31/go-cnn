from gomill import boards, ascii_boards
from keras.models import load_model
from parse_sgfs import board_to_nn
import numpy as np
from keras.utils import np_utils
import parse_sgfs

model = load_model("model.h5")
board = boards.Board(19)

def zero_illegal(board, weights):
    for x in range(19):
        for y in range(19):
            pos = board.get(x, y)

            if not pos is None:
                weights[0][x + 19 * y] = -1

while True:
    print ascii_boards.render_board(board)
    try:
        board.play(row=input("x: "), col=input("y: "), colour='b')
    except:
        continue

    y = model.predict(np.array([board_to_nn(board, 'w')]))
    print y
    zero_illegal(board, y)

    i = np.argmax(y[0])


    print (i % 19, i // 19)
    board.play(row=i % 19, col=i // 19, colour='w')
