import unittest

import numpy as np

from runforthetop.RunForTheTopGame import RunForTheTopGame
from runforthetop.RunForTheTopBoard import Board


class RunForTheTopTests(unittest.TestCase):
    def xtest_display(self):
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
        for move in moves:
            encoded = RunForTheTopGame._from_move_to_numpy_action(move)
            decoded = RunForTheTopGame._from_numpy_action_to_move(encoded)
            self.assertEqual(move, decoded, "encoding and decoding should be inverse operations")

    #
    #    0 1 2 3 4 5 6 7
    # -----------------------
    # 0 |- - - - - - - - |
    # 1 |- - - - - - - - |
    # 2 |- - - - - - - - |
    # 3 |- - - - - - - - |
    # 4 |- - - - - - - - |
    # 5 |- - - - - - - - |
    # 6 |- - - - - - - - |
    # 7 |- - O O X X - - |
    # -----------------------
    def test_game_not_ended_at_start(self):
        game = RunForTheTopGame()
        initial_state = game.getInitBoard()
        self.assertEqual(0, game.getGameEnded(initial_state, 1), "game should not be ended")
        self.assertEqual(0, game.getGameEnded(initial_state, -1), "game should not be ended for either player")

    def test_game_not_ended_with_one_piece_above_the_line(self):
        game = RunForTheTopGame()
        board = Board()
        board.set((7, 2), 0)
        board.set((3, 2), 1)
        s = board.state()
        self.assertEqual(0, game.getGameEnded(s, 1), "both pieces should be above the line to win")
        self.assertEqual(0, game.getGameEnded(s, -1), "...for either player")

    def test_both_pieces_must_be_above_the_line_to_win(self):
        game = RunForTheTopGame()
        board = Board()
        board.set((7, 2), 0)
        board.set((3, 2), 1)
        board.set((7, 3), 0)
        board.set((3, 3), 1)
        s = board.state()
        self.assertEqual(1, game.getGameEnded(s, 1), "player 1 won")
        self.assertEqual(-1, game.getGameEnded(s, -1), "player -1 lost")

    def test_game_ended_for_other_player(self):
        game = RunForTheTopGame()
        board = Board()
        board.set((7, 4), 0)
        board.set((7, 5), 0)
        board.set((3, 4), -1)
        board.set((3, 5), -1)
        s = board.state()
        self.assertEqual(1, game.getGameEnded(s, -1), "player -1 won")
        self.assertEqual(-1, game.getGameEnded(s, 1), "player 1 lost")

