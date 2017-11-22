from gomill import sgf, boards
import glob
import numpy as np
import random as rnd

def main():
    print parse_all()


def parse_all():
    datax = []
    datay = []
    for file in get_sgfs():
        try:
            x, y = parse_sgf(file)
            datax += x
            datay += y
        except:
            print "parse error", file
    return (datax, datay)


def parse_sgf(file):
    with open(file) as fh:
        g = sgf.Sgf_game.from_string(fh.read())

    mainseq = g.get_main_sequence()

    mainseq = mainseq[1:]

    datax = []
    datay = []

    curr = boards.Board(19)

    for node in mainseq:
        if node.has_property("W"):
            move = node.get("W")
            pos, move = make_case(curr, move, 'w')
            datax.append(pos)
            datay.append(move)
            curr.play(move[0], move[1], 'w')
        elif node.has_property("B"):
            move = node.get("B")
            pos, move = make_case(curr, move, 'w')
            datax.append(pos)
            datay.append(move)
            curr.play(move[0], move[1], 'b')
    return (datax, datay)


def make_case(curr, move, color):
    return (board_to_nn(curr, color), move)


def board_to_nn(board, color):

    posarr = [[(0, 0) for x in range(board.side)] for y in range(board.side)]

    for x in range(board.side):
        for y in range(board.side):
            pos = board.get(x, y)

            if pos is None:
                continue

            if pos == color:
                posarr[x][y] = (1, 0)
            elif pos != color:
                posarr[x][y] = (0, 1)

    return np.array(posarr)


def get_sgfs():
    return glob.glob("./sgfs/*.sgf")


if __name__ == "__main__":
    main()
