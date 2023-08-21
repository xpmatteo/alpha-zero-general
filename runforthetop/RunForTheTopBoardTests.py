import unittest
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
        expected = [(a, (6, 1)), (a, (6, 2)), (a, (6, 3)), (b, (6, 2)), (b, (6, 3)), (b, (6, 4)),
                    (a, (7, 1))]
        self.assertEqual(set(expected), set(board.get_legal_moves(1)))

    def test_execute_move(self):
        board = Board()
        board.execute_move(((7, 2), (6, 1)), 1)
        self.assertEqual(1, board[6][1])
        self.assertEqual(0, board[7][2])
