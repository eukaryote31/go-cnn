from gomill import boards, common
from play import zero_illegal
from keras.models import load_model
from parse_sgfs import board_to_nn
import numpy as np

def main():
    player = GTP()

    while True:
        inp = raw_input()
        cmd = inp.split(" ")
        print getattr(player, cmd[0])(cmd) + "\n"


class GTP:

    def __init__(self):
        self.board = boards.Board(19)
        self.model = load_model("model.h5")
        self.moves = []

    def name(self, cmd):
        return "= NN Go"

    def version(self, cmd):
        return "= 0.1"

    def protocol_version(self, cmd):
        return "= 2"

    def list_commands(self, cmd):
        return """
        name
        version
        protocol_version
        list_commands
        boardsize
        clear_board
        play
        genmove
        """

    def boardsize(self, cmd):
        if not cmd[0] == "19":
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
        y = self.model.predict(np.array([board_to_nn(self.board, cmd[1].lower(), self.moves)]))
        zero_illegal(self.board, y)

        i = np.argmax(y[0])
        self.board.play(row=i % 19, col=i // 19, colour=cmd[1].lower())
        self.moves.append((i % 19, i // 19))
        return "= " + common.format_vertex((i % 19, i // 19))


if __name__ == "__main__":
    main()
