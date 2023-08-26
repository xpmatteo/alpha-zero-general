import unittest
import numpy as np
from runforthetop.RunForTheTopBoard import Board


class RunForTheTopLogicTests(unittest.TestCase):
    def test_adjacent_squares(self):
        board = Board()
        actual = board._adjacent_squares((2, 4))
        expected = [(3, 3), (3, 4), (3, 5),
                    (2, 3),         (2, 5),
                    (1, 3), (1, 4), (1, 5)]
        self.assertEqual(set(expected), set(actual))

    def test_adjacent_valid_squares(self):
        board = Board()
        expected = [(1, 0), (1, 1),
                            (0, 1)]
        self.assertEqual(set(expected), set(board._adjacent_on_board_squares((0, 0))))

    def test_available_moves_from_square(self):
        board = Board()
        a = (7, 2)
        expected = [(a, (6, 1)), (a, (6, 2)), (a, (6, 3)),
                    (a, (7, 1))]
        self.assertEqual(set(expected), set(board._available_moves_from_square(a)))
        b = (7, 3)
        expected = [(b, (6, 2)), (b, (6, 3)), (b, (6, 4))]
        self.assertEqual(set(expected), set(board._available_moves_from_square(b)))

    def test_available_moves_in_initial_board(self):
        """
    0 1 2 3 4 5 6 7
-----------------------
0 |- - - - - - - - |
1 |- - - - - - - - |
2 |- - - - - - - - |
3 |- - - - - - - - |
4 |- - - - - - - - |
5 |- - - - - - - - |
6 |- - - - - - - - |  X = -1
7 |- - O O X X - - |  O = +1
-----------------------
        """
        board = Board()
        a = (7, 2)
        b = (7, 3)
        expected = [(a, (6, 1)), (a, (6, 2)), (a, (6, 3)), (b, (6, 2)), (b, (6, 3)), (b, (6, 4)), (a, (7, 1))]
        self.assertEqual(set(expected), set(board.get_legal_moves(1)))
        c = (7, 4)
        d = (7, 5)
        expected = [(c, (6, 3)), (c, (6, 4)), (c, (6, 5)), (d, (6, 4)), (d, (6, 5)), (d, (6, 6)), (d, (7, 6))]
        self.assertEqual(set(expected), set(board.get_legal_moves(-1)))

    def test_execute_move(self):
        board = Board()
        board.execute_move(((7, 2), (6, 1)), 1)
        self.assertEqual(1, board[6][1])
        self.assertEqual(0, board[7][2])

    def test_state(self):
        board = Board()
        state = board.state()
        self.assertEqual(1, state[7][2])
        self.assertEqual(1, state[7][3])
        self.assertEqual(-1, state[7][4])
        self.assertEqual(-1, state[7][5])
        self.assertEqual(0, state[0][0])

    def test_from_state(self):
        board = Board()
        state = board.state()
        board2 = Board.fromState(state)
        self.assertTrue(np.all(board.state() == board2.state()))

    def test_clone_state(self):
        board = Board()
        state = board.state()
        board2 = Board.cloneState(state)
        board2_state = board2.state()
        state[7][2] = 0
        self.assertEqual(1, board2_state[7][2])
