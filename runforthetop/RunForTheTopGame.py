from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .RunForTheTopBoard import Board
import numpy as np

class RunForTheTopGame(Game):
    square_display_rep = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    def __init__(self):
        super().__init__()
        self.n = 8
        self.N_FOURTH_POWER = 8**4
        self.N_CUBE = 8**3
        self.N_SQUARE = 8**2

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        """
        Moves are of the form (from_square, to_square).
        The number of actions is the number of squares on the board, squared,
        plus 1 for pass
        """
        return self.N_FOURTH_POWER + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self._pass_action():
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)        
        move = self._from_numpy_action_to_move(action)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        valids[-1] = 1 # pass is always allowed
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        for move in legalMoves:
            valids[self._from_move_to_numpy_action(move)] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        if b.countDiff(player) > 0:
            return 1
        return -1

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_display_rep[square] for row in board for square in row)
        return board_s

    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    @staticmethod
    def displayContent(board):
        n = board.shape[0]
        result = ""
        result += "   "
        for y in range(n):
            result += str(y) + " "
        result += "\n"
        result += "-----------------------\n"
        for y in range(n):
            result += str(y) + " |"   # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                result += RunForTheTopGame.square_display_rep[piece] + " "

            result += "|\n"
        result += "-----------------------\n"
        return result

    @staticmethod
    def display(board):
        print(RunForTheTopGame.displayContent(board))

    def _pass_action(self):
        """The last action in the numpy array of actions is always pass"""
        return self.N_FOURTH_POWER

    def _from_move_to_numpy_action(self, move):
        """We encode the move as a base N number, where N is the board side length."""
        (r1, c1), (r2, c2) = move
        return r1 + c1 * self.n + r2 * self.N_SQUARE + c2 * self.N_CUBE

    def _from_numpy_action_to_move(self, action):
        c2 = action // self.N_CUBE
        action = action % self.N_CUBE
        r2 = action // self.N_SQUARE
        action = action % self.N_SQUARE
        c1 = action // self.n
        r1 = action % self.n
        return ((r1, c1), (r2, c2))

