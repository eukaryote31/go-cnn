from gomill import sgf, boards
import glob
import numpy as np
import numpy.random as npr
import random as rnd
import math
import cPickle as pickle


def main():
    print "parsing..."
    parsed = parse_all()
    print "pickling"
    with open("dataset.pickle", "wb") as fh:
        pickle.dump(parsed, fh, protocol=2)

    print "pickled!"


def parse_all():
    datax = []
    datay = []
    i = 0
    for file in get_sgfs():
        print "parsed", i
        x, y = parse_sgf(file)
        datax += x
        datay += y
        i += 1

    return (datax, datay)


def parse_sgf(file):
    with open(file) as fh:
        g = sgf.Sgf_game.from_string(fh.read())

    mainseq = g.get_main_sequence()

    mainseq = mainseq[1:]

    datax = []
    datay = []

    curr = boards.Board(19)

    moves = []
    for node in mainseq:
        if node.has_property("W"):
            move = node.get("W")
            pos, move = make_case(curr, move, 'w', moves)
            datax.append(pos)
            datay.append(move)
            curr.play(move[0], move[1], 'w')
        elif node.has_property("B"):
            move = node.get("B")
            pos, move = make_case(curr, move, 'w', moves)
            datax.append(pos)
            datay.append(move)
            curr.play(move[0], move[1], 'b')
        moves.append(move)
    zipped = zip(datax, datay)
    zipped = rnd.sample(zipped, 5)
    datax, datay = zip(*zipped)
    return (datax, datay)


def make_case(curr, move, color, moves):
    return (board_to_nn(curr, color, moves), move)


def board_to_nn(board, color, moves):

    posarr = [[(0, 0, 0, 0) for x in range(board.side)]
              for y in range(board.side)]

    for x in range(board.side):
        for y in range(board.side):
            pos = board.get(x, y)

            if pos in moves:
                n = moves.index(pos)
            else:
                n = 0

            if pos is None:
                continue

            # (same, opponent, movenum)
            if pos == color:
                posarr[x][y] = (1, 0, n, simple_liberties(board, x, y))
            elif pos != color:
                posarr[x][y] = (0, 1, n, simple_liberties(board, x, y))

    return np.array(posarr)


def simple_liberties(board, x, y):
    n = 0
    if x > 0 and board.get(x - 1, y) is None:
        n += 1
    if y > 0 and board.get(x, y - 1) is None:
        n += 1
    if x < 18 and board.get(x + 1, y) is None:
        n += 1
    if y < 18 and board.get(x, y + 1) is None:
        n += 1
    return n


def get_sgfs():
    return glob.glob("./sgfs/*.sgf")


if __name__ == "__main__":
    main()
