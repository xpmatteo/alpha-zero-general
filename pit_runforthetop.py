import argparse

import Arena
from MCTS import MCTS
from runforthetop.RunForTheTopPlayers import *
from runforthetop.keras.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

parser = argparse.ArgumentParser()
parser.add_argument("--num_plays", type=int, default=2, help="number of games to run for")
parser.add_argument("--human", action="store_true", default=False, help="human vs cpu")
parser.add_argument("--mcts_iterations", type=int, default=50, help="number of MCTS iterations")
args = parser.parse_args()

human_vs_cpu = args.human

g = Game()

# all players
rp = RandomPlayer(g).play
gp = GreedyPlayer(g).play
hp = HumanPlayer(g).play

# nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp', 'best.keras')
args1 = dotdict({'numMCTSSims': args.mcts_iterations, 'cpuct': 1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./temp', 'best.keras')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=Game.display)

print(arena.playGames(args.num_plays, verbose=True))
