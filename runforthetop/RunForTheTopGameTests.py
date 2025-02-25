import unittest

import numpy as np

from runforthetop.RunForTheTopGame import RunForTheTopGame
from runforthetop.RunForTheTopBoard import Board


class RunForTheTopTests(unittest.TestCase):
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

    def test_get_next_state_move(self):
        game = RunForTheTopGame()
        board = game.getInitBoard()
        player = 1
        action = RunForTheTopGame._from_move_to_numpy_action(((7, 2), (6, 1)))
        new_state, new_player = game.getNextState(board, player, action)
        self.assertEqual(-1, new_player, "player should be switched")
        new_board = Board.fromState(new_state)
        self.assertEqual(0, new_board[(7, 2)], "old position should be empty")
        self.assertEqual(1, new_board[(6, 1)], "new position should be occupied")

    def test_available_moves(self):
        game = RunForTheTopGame()
        moves = game.getValidMoves(game.getInitBoard(), 1)
        self.assertEqual(8*8*8*8 + 1, len(moves), "should be one move per square squared plus pass")
        self.assertEqual(0, moves[8**4], "Pass is not a valid move")

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
        board.moveUnit((7, 2), (3, 2))
        s = board.state()
        self.assertEqual(0, game.getGameEnded(s, 1), "both pieces should be above the line to win")
        self.assertEqual(0, game.getGameEnded(s, -1), "...for either player")

    def test_both_pieces_must_be_above_the_line_to_win(self):
        game = RunForTheTopGame()
        board = Board()
        board.moveUnit((7, 2), (3, 2))
        board.moveUnit((7, 3), (3, 3))
        s = board.state()
        self.assertEqual(1, game.getGameEnded(s, 1), "player 1 won")
        self.assertEqual(-1, game.getGameEnded(s, -1), "player -1 lost")

    def test_game_ended_for_other_player(self):
        game = RunForTheTopGame()
        board = Board()
        board.moveUnit((7, 4), (3, 4))
        board.moveUnit((7, 5), (3, 5))
        s = board.state()
        self.assertEqual(1, game.getGameEnded(s, -1), "player -1 won")
        self.assertEqual(-1, game.getGameEnded(s, 1), "player 1 lost")

