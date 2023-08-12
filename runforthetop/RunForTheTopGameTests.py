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
        pieces, new_player = game.getNextState(board, player, action)
        self.assertEqual(board, game.getInitBoard(), "original board should not be modified")

    def test_available_moves(self):
        game = RunForTheTopGame()
        moves = game.getValidMoves(game.getInitBoard(), 1)
        self.assertEqual(8*8*8*8 + 1, len(moves), "should be one move per square squared plus pass")
        self.assertEqual(1, moves[8**4], "Pass is always a valid move")

    def test_encode_and_decode_of_moves(self):
        moves = [
            ((3, 7), (1, 4))
            , ((0, 0), (0, 0))
            , ((7, 7), (7, 7))
        ]
        game = RunForTheTopGame()
        for move in moves:
            encoded = game._from_move_to_numpy_action(move)
            decoded = game._from_numpy_action_to_move(encoded)
            self.assertEqual(move, decoded, "encoding and decoding should be inverse operations")



