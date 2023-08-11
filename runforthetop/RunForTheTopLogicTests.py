import unittest
from runforthetop.RunForTheTopLogic import Board


class RunForTheTopLogicTests(unittest.TestCase):
    def test_available_moves(self):
        """
    0 1 2 3 4 5 6 7
-----------------------
0 |- - - - - - - - |
1 |- - - - - - - - |
2 |- - - - - - - - |
3 |- - - - - - - - |
4 |- - - - - - - - |
5 |- - - - - - - - |
6 |- - - - - - - - |
7 |- - O O X X - - |
-----------------------
        """
        board = Board()
        actual = board.get_legal_moves(1)
        expected = [()]
        self.assertEqual(expected, actual)


