from gomill import boards, common
from play import zero_illegal
from keras.models import load_model
from parse_sgfs import board_to_nn
import numpy as np
from gtp import Engine
import sys
from policy import NNPolicy

def main():
    engine = Engine(game_obj=NNGame(), name='NNGo', version='0.1')
    while True:
        sys.stdout.write(engine.send(sys.stdin.readline().strip()))


def main():
    player = GTP()

    while True:
        inp = sys.stdin.readline().strip()
        cmd = inp.split(" ")
        sys.stdout.write(getattr(player, cmd[0])(cmd) + "\n\n")
        sys.stdout.flush()


class GTP:

    def __init__(self):
        self.board = boards.Board(19)
        self.moves = []
        self.policy = NNPolicy('model.h5')

    def name(self, cmd):
        return "= NN Go"

    def version(self, cmd):
        return "= 0.1"

    def protocol_version(self, cmd):
        return "= 2"

    def list_commands(self, cmd):
        return """= name
version
protocol_version
list_commands
boardsize
clear_board
play
genmove"""

    def boardsize(self, cmd):
        if not cmd[1] == "19":
            return "= BOARDSIZE NOT SUPPORTED"
        return "="

    def clear_board(self, cmd):
        self.board = boards.Board(19)
        return "="

    def play(self, cmd):
        x, y = common.move_from_vertex(cmd[2], 19)
        self.board.play(row=x, col=y, colour=cmd[1].lower())
        self.moves.append((x, y))
        return "="

    def genmove(self, cmd):
        y = self.policy.evaluate(self.board, cmd[1].lower(), self.moves)

        i = np.argmax(y[0])
        self.board.play(row=i % 19, col=i // 19, colour=cmd[1].lower())
        self.moves.append((i % 19, i // 19))
        return "= " + common.format_vertex((i % 19, i // 19))


if __name__ == "__main__":
    main()
