from gomill.boards import Board


class MCTree:

    def __init__(self, policy, value):
        self.policy = policy
        self.value = value
        self.rootnode = TreeNode(Board(19), None, [], None, None)



class TreeNode:

    def __init__(self, board, move, moves, color, parent):
        self.board = board
        self.color = colour
        self.move = move
        self.moves = moves
        self.parent = parent

    def populate_child_nodes(self, policy):


    def get_legal_moves(self, board, color):
        ret = []
        for x in range(19):
            for y in range(19):
                pos = self.board.get(x, y)

                # KO
                if len(moves) > 2 and moves[-2] == pos:
                    continue

                if pos is None:
                    # suicide rule
                    if x > 0 and board.get(x - 1, y) is None:
                        ret.append((x, y))
                        continue
                    if y > 0 and board.get(x, y - 1) is None:
                        ret.append((x, y))
                        continue
                    if x < 18 and board.get(x + 1, y) is None:
                        ret.append((x, y))
                        continue
                    if y < 18 and board.get(x, y + 1) is None:
                        ret.append((x, y))
                        continue

                    boardcopy = self.board.copy()
                    boardcopy.play(x, y, color)
                    if boardcopy.get(x, y) is not None:
                        ret.append((x, y))
        return ret
