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

class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        actions = self.game.getValidMoves(board, 1)
        valid_actions = []
        for i in range(len(actions)):
            if actions[i]:
                valid_actions.append(i)
        for i in range(len(valid_actions)):
            if i == len(valid_actions) - 1:
                print("%2d: %s" % (i, "pass"))
            else:
                print("%2d: %s" % (i, Game._from_numpy_action_to_move(valid_actions[i])))
        while True:
            try:
                input_move = valid_actions[int(input())]
                if actions[input_move]:
                    break
            except ValueError:
                # Input needs to be an integer
                'Invalid integer'
            print('Invalid move')
        return input_move


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
