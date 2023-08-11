import unittest

import numpy as np

from runforthetop.RunForTheTopGame import RunForTheTopGame


class RunForTheTopTests(unittest.TestCase):
    def test_display(self):
        game = RunForTheTopGame()
        display = game.displayContent(game.getInitBoard())
        print(display)

    def test_action_size(self):
        game = RunForTheTopGame()
        self.assertEqual(game.getActionSize(), 8*8*8*8 + 1)

    def test_get_next_state_pass(self):
        game = RunForTheTopGame()
        board = game.getInitBoard()
        player = 1
        action = 8**4
        pieces, new_player = game.getNextState(board, player, action)
        self.assertEqual(-1, new_player, "player should be switched")
        self.assertTrue(np.all(board == pieces), "board should not be modified")

    def xtest_get_next_state_move(self):
        game = RunForTheTopGame()
        board = game.getInitBoard()
        player = 1
        action = ((7, 2), (6, 1))
        next_state = game.getNextState(board, player, action)
        self.assertEqual(board, game.getInitBoard(), "original board should not be modified")

    def xtest_available_moves(self):
        game = RunForTheTopGame(8)
        moves = game.getValidMoves(game.getInitBoard(), 1)
        self.assertEqual(moves, [8, 9, 10, 11])



