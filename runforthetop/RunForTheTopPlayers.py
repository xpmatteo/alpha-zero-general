import numpy as np
from .RunForTheTopGame import RunForTheTopGame as Game

# non-human players always play as Player 1
NON_HUMAN_PLAYER_NUMBER = 1


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, NON_HUMAN_PLAYER_NUMBER)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


def clean_input_move(input_move):
    return input_move \
        .replace("(", " ") \
        .replace(")", " ") \
        .replace(",", " ")


class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print("[", Game._from_numpy_action_to_move(i), end="] ")
        while True:
            input_move = input()
            input_a = clean_input_move(input_move).split()
            if len(input_a) == 4:
                try:
                    x1,y1,x2,y2 = [int(i) for i in input_a]
                    move = ((x1,y1), (x2, y2))
                    action = Game._from_move_to_numpy_action( move )
                    if valid[action]:
                        break
                except ValueError:
                    # Input needs to be an integer
                    'Invalid integer'
            print('Invalid move')
        return action


class GreedyPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
