# -*- encoding: utf-8 -*-
from gomill import boards, ascii_boards, common, sgf
from keras.models import load_model
from parse_sgfs import board_to_nn
import numpy as np
from keras.utils import np_utils
import parse_sgfs
from main import board_loss
import keras.losses
import math

model = load_model("model.h5", custom_objects={'board_loss': board_loss})
board = boards.Board(19)

SELFPLAY = False

def zero_illegal(board, weights):
    for x in range(19):
        for y in range(19):
            pos = board.get(x, y)

            if not pos is None:
                weights[0][x + 19 * y] = 0


def normalized(a):
    return a


moves = []
with open("play_st.sgf", "r") as fh:
    g = sgf.Sgf_game.from_string(fh.read())

    mainseq = g.get_main_sequence()

    mainseq = mainseq[1:]
    for node in mainseq:
        if len(moves) >= 0:
            break
        if node.has_property("W"):
            move = node.get("W")
            board.play(move[0], move[1], 'w')
        elif node.has_property("B"):
            move = node.get("B")
            board.play(move[0], move[1], 'b')
        moves.append(move)

prob_disp = [' ', ' ', '░', '░', '▒', '▒', '▓', '▓', '█', '█']
while True:
    print ascii_boards.render_board(board)
    if not SELFPLAY:
        m = raw_input("move: ")
        print m
        playerpos = common.move_from_vertex(m, 19)
        moves.append(playerpos)
        board.play(row=playerpos[0], col=playerpos[1], colour='b')
    else:
        if len(moves) > 200:
            break

    y = model.predict(np.array([board_to_nn(board, 'w', moves)]))
    zero_illegal(board, y)

    probs = np.reshape(normalized(y[0]), (19, 19))
    print probs
    print sum(sum(probs))
    for ax in range(19):
        r = ""
        for ay in range(19):
            r += str(prob_disp[int(probs[ax][ay] * 10)]) * 2
        print r

    i = np.argmax(y[0])

    moves.append((i % 19, i // 19))
    comp_color = 'w'
    if SELFPLAY and len(moves) % 2 == 1:
        comp_color = 'b'
    board.play(row=i % 19, col=i // 19, colour=comp_color)
