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

    def xtest_available_moves_in_initial_board(self):
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
        actual = board.get_legal_moves(1)
        expected = [(6, 2), (6, 3)]
        self.assertEqual(expected, actual)


