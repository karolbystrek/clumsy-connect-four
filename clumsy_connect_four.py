try:
    import numpy as np
except ImportError:
    print("Sorry, this example requires Numpy installed !")
    raise

from easyAI import TwoPlayerGame


class ConnectFour(TwoPlayerGame):
    """
    The game of Connect Four, as described here:
    http://en.wikipedia.org/wiki/Connect_Four
    """

    def __init__(self, players, board=None, slip_probability=0.0):
        self.players = players
        self.slip_probability = slip_probability
        self.board = (
            board
            if (board is not None)
            else (np.array([[0 for i in range(7)] for j in range(6)]))
        )
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def play(self, nmoves=1000, verbose=True):
        from copy import deepcopy
        history = []

        if verbose:
            self.show()

        for self.nmove in range(1, nmoves + 1):
            if self.is_over():
                break

            move = self.player.ask_move(self)
            history.append((deepcopy(self), move))
            
            actual_move = self.slip_move(move)
            self.make_move(actual_move)

            if verbose:
                print(
                    "\nMove #%d: player %d plays %s :"
                    % (self.nmove, self.current_player, str(actual_move))
                )
                self.show()

            self.switch_player()

        history.append(deepcopy(self))
        return history

    def make_move(self, column):
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.current_player
    
    def slip_move(self, column):
        if np.random.random() < self.slip_probability:
            adjacent = []
            if column > 0:
                adjacent.append(column - 1)
            if column < 6:
                adjacent.append(column + 1)
            
            valid_adjacent = [c for c in adjacent if self.board[:, c].min() == 0]
            
            if valid_adjacent:
                print("Slip!")
                return np.random.choice(valid_adjacent)
        return column

    def show(self):
        print(
            "\n"
            + "\n".join(
                ["0 1 2 3 4 5 6", 13 * "-"]
                + [
                    " ".join([[".", "O", "X"][self.board[5 - j][i]] for i in range(7)])
                    for j in range(6)
                ]
            )
        )

    def lose(self):
        return find_four(self.board, self.opponent_index)

    def is_over(self):
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0


def find_four(board, current_player):
    """
    Returns True iff the player has connected  4 (or more)
    This is much faster if written in C or Cython
    """
    for pos, direction in POS_DIR:
        streak = 0
        while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
            if board[pos[0], pos[1]] == current_player:
                streak += 1
                if streak == 4:
                    return True
            else:
                streak = 0
            pos = pos + direction
    return False


POS_DIR = np.array(
    [[[i, 0], [0, 1]] for i in range(6)]
    + [[[0, i], [1, 0]] for i in range(7)]
    + [[[i, 0], [1, 1]] for i in range(1, 3)]
    + [[[0, i], [1, 1]] for i in range(4)]
    + [[[i, 6], [1, -1]] for i in range(1, 3)]
    + [[[0, i], [1, -1]] for i in range(3, 7)]
)
