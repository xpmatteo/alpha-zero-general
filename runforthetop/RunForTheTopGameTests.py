import unittest
from runforthetop.RunForTheTopGame import RunForTheTopGame


class RunForTheTopTests(unittest.TestCase):
    def test_display(self):
        game = RunForTheTopGame(8)
        display = game.displayContent(game.getInitBoard())
        print(display)

    def test_available_moves(self):
        game = RunForTheTopGame(8)
        moves = game.getValidMoves(game.getInitBoard(), 1)
        self.assertEqual(moves, [8, 9, 10, 11])



