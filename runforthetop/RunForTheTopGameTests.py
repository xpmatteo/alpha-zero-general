import unittest
from runforthetop.RunForTheTopGame import RunForTheTopGame
from io import StringIO
from unittest.mock import patch


INITIAL_BOARD = """
   0 1 2 3 4 5 6 7
"""

XINITIAL_BOARD = """
   0 1 2 3 4 5 6 7
-----------------------
0 |- - - - - - - - |
1 |- - - - - - - - |
2 |- - - - - - - - |
3 |- - - X O - - - |
4 |- - - O X - - - |
5 |- - - - - - - - |
6 |- - - - - - - - |
7 |- - - - - - - - |
-----------------------
"""

class RunForTheTopTests(unittest.TestCase):
    def test_display(self):
        unittest.util._MAX_LENGTH=2000
        game = RunForTheTopGame(8)
        display = game.displayContent(game.getInitBoard())
        print(display)




