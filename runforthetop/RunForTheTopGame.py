from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .RunForTheTopBoard import Board
import numpy as np

BOARD_SIDE = 8
BOARD_SIDE_SQUARE = 8**2
BOARD_SIDE_CUBE = 8**3
BOARD_SIDE_FOURTH_POWER = 8**4


class RunForTheTopGame(Game):
    square_display_rep = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    def __init__(self):
        super().__init__()

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(BOARD_SIDE)
        return b.state()

    def getBoardSize(self):
        return (BOARD_SIDE, BOARD_SIDE)

    def getActionSize(self):
        """
        Moves are of the form (from_square, to_square).
        The number of actions is the number of squares on the board, squared,
        plus 1 for pass
        """
        return BOARD_SIDE_FOURTH_POWER + 1

    def getNextState(self, state, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self._pass_action():
            return (state, -player)
        b = Board.cloneState(state)
        move = RunForTheTopGame._from_numpy_action_to_move(action)
        b.execute_move(move, player)
        return (b.state(), -player)

    def getValidMoves(self, state, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        valids[-1] = 0
        b = Board.cloneState(state)
        legalMoves = b.get_legal_moves(player)
        for move in legalMoves:
            valids[RunForTheTopGame._from_move_to_numpy_action(move)] = 1
        return np.array(valids)

    def getGameEnded(self, state, player):
        """return 0 if not ended, 1 if the given player won, -1 if the given player lost"""
        b = Board.fromState(state)
        return player * b.game_status()

    def getCanonicalForm(self, state, player):
        """
        The "canonical form" of the board is the board as presented to the neural network.
        In order for the NN to learn, it must always be presented with "1" as "the pieces you move"
        """
        return Board.getCanonicalForm(state, player)

    def getSymmetries(self, state, pi):
        return [(state, pi)]

    def stringRepresentation(self, state):
        return state.tostring()

    def stringRepresentationReadable(self, state):
        board_s = "".join(self.square_display_rep[square] for row in state for square in row)
        return board_s

    @staticmethod
    def displayContent(state):
        n = 8
        b = Board.fromState(state)
        result = ""
        result += "   "
        for y in range(n):
            result += str(y) + " "
        result += "\n"
        result += "-----------------------\n"
        for y in range(n):
            result += str(y) + " |"   # print the row #
            for x in range(n):
                piece = b[(y, x)]    # get the piece to print
                result += RunForTheTopGame.square_display_rep[piece] + " "

            result += "|\n"
        result += "-----------------------\n"
        return result

    @staticmethod
    def display(state):
        print(RunForTheTopGame.displayContent(state))

    def _pass_action(self):
        """The last action in the numpy array of actions is always pass"""
        return BOARD_SIDE_FOURTH_POWER

    @staticmethod
    def _from_move_to_numpy_action(move):
        """We encode the move as a base N number, where N is the board side length."""
        (r1, c1), (r2, c2) = move
        return r1 + c1 * BOARD_SIDE + r2 * BOARD_SIDE_SQUARE + c2 * BOARD_SIDE_CUBE

    @staticmethod
    def _from_numpy_action_to_move(action):
        c2 = action // BOARD_SIDE_CUBE
        action = action % BOARD_SIDE_CUBE
        r2 = action // BOARD_SIDE_SQUARE
        action = action % BOARD_SIDE_SQUARE
        c1 = action // BOARD_SIDE
        r1 = action % BOARD_SIDE
        return ((r1, c1), (r2, c2))

