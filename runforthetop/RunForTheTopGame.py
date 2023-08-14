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
        return b.state()

    def getBoardSize(self):
        return (self.n, self.n)

    def getActionSize(self):
        """
        Moves are of the form (from_square, to_square).
        The number of actions is the number of squares on the board, squared,
        plus 1 for pass
        """
        return self.N_FOURTH_POWER + 1

    def getNextState(self, state, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self._pass_action():
            return (state, -player)
        b = Board.cloneState(state)
        move = self._from_numpy_action_to_move(action)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, state, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        valids[-1] = 1 # pass is always allowed
        b = Board.cloneState(state)
        legalMoves = b.get_legal_moves(player)
        for move in legalMoves:
            valids[self._from_move_to_numpy_action(move)] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        """return 0 if not ended, 1 if the given player won, -1 if the given player lost"""
        b = Board.fromState(board)
        return player * b.game_status()

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        return [(board,pi)]

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_display_rep[square] for row in board for square in row)
        return board_s

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

