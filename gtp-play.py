from gomill import boards, common
from play import zero_illegal
from keras.models import load_model
from parse_sgfs import board_to_nn
import numpy as np
from gtp import Engine
import sys

def main():
    engine = Engine(game_obj=NNGame(), name='NNGo', version='0.1')
    while True:
        sys.stdout.write(engine.send(sys.stdin.readline().strip()))
    model = load_model("model.h5")


class NNGame(object):

    def __init__(self, komi=6.5):
        self.komi = komi
        self.board = boards.Board(19)
        self.moves = []

    def clear(self):
        self.board = boards.Board(19)
        self.moves = []

    def make_move(self, color, vertex):
        x, y = common.move_from_vertex(np.subtract(vertex, (1, 1)), 19)
        try:
            self.board.play(row=x, col=y, colour=color.lower())
        except:
            return False
        self.moves.append((x, y))
        return True

    def set_size(self, n):
        if n != 19:
            return False
        else:
            self.clear()

    def set_komi(self, k):
        self.komi = k

    def get_move(self, color):
        return (0,0)
        y = model.predict(np.array([board_to_nn(self.board, color.lower(), self.moves)]))
        zero_illegal(self.board, y)

        i = np.argmax(y[0])
        self.board.play(row=i % 19, col=i // 19, colour=color.lower())
        self.moves.append((i % 19, i // 19))
        return (i % 19 + 1, i // 19 + 1)


if __name__ == "__main__":
    main()
