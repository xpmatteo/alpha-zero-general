import unittest
from runforthetop.RunForTheTopBoard import Board


class RunForTheTopLogicTests(unittest.TestCase):
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
        actual = board.get_legal_moves(1)
        expected = [(6, 2), (6, 3)]
        self.assertEqual(expected, actual)


