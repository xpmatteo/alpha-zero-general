import numpy as np


class Unit():
    def __init__(self, color):
        self.color = color


class Board():
    """
    Author: Eric P. Nichols; modified by Matteo Vaccari
    Squares are stored and manipulated as (r,c) tuples,
    where r is the row, c is the col.
    Moves are pairs of the form (from_square, to_square).
    """

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n=8):
        """Set up initial board configuration."""
        self.n = n
        self.units = {
                (7, 2): Unit(1),
                (7, 3): Unit(1),
                (7, 4): Unit(-1),
                (7, 5): Unit(-1),
        }

    @classmethod
    def fromState(cls, state):
        board = Board()
        board.units = state
        return board

    @classmethod
    def cloneState(cls, state):
        board = Board()
        board.units = state.copy()
        return board

    def state(self):
        return self.units

    def __getitem__(self, index):
        """add [(r, c)] indexer syntax to the Board"""
        if index in self.units:
            return self.units[index].color
        return 0

    def at(self, square):
        """ get square color from a pair (r,c) """
        return self[(square[0],square[1])]

    # def set(self, square, color):
    #     """ set color of square (r,c)"""
    #     self[square[0]][square[1]] = color

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        1 for white O, -1 for black X
        """
        moves = set()  # stores the legal moves.
        # Get all the squares with pieces of the given color.
        for c in range(self.n):
            for r in range(self.n):
                if self[(r, c)] == color:
                    newmoves = self._available_moves_from_square((r,c))
                    moves.update(newmoves)
        return list(moves)

    def execute_move(self, move, player):
        from_square, to_square = move
        self.moveUnit(from_square, to_square)

    def game_status(self):
        player1 = 0
        player_minus1 = 0
        for r in range(0, self.n // 2):
            for c in range(self.n):
                if self[(r, c)] == 1:
                    player1 += 1
                elif self[(r, c)] == -1:
                    player_minus1 += 1
        if player1 == 2:
            return 1
        elif player_minus1 == 2:
            return -1
        else:
            return 0

    def placeUnit(self, unit, square):
        if self.unit_is_present(unit):
            raise Exception('Unit added twice')
        if square in self.units:
            raise Exception(f'Unit already exists at ${square}')
        if self.out_of_bounds(square):
            raise Exception(f'Square ${square} outside of map')
        self.units[square] = unit

    def moveUnit(self, from_square, to_square):
        if from_square not in self.units:
            raise ValueError(f'No unit at ${from_square}')
        if to_square == from_square:
            return
        if to_square in self.units:
            raise ValueError(f'Unit already exists at ${to_square}');
        self.units[to_square] = self.units[from_square]
        del self.units[from_square]

    def unit_is_present(self, unit):
        return unit in self.units.values()

    def out_of_bounds(self, square):
        return square[0] < 0 or square[0] >= self.n or square[1] < 0 or square[1] >= self.n

    def _adjacent_squares(self, square):
        """ Returns the list of squares adjacent to the given square """
        return [self._add_square(square, direction) for direction in self.__directions]

    @staticmethod
    def _add_square(square, direction):
        return (square[0]+direction[0], square[1]+direction[1])

    def _adjacent_on_board_squares(self, from_square):
        return [square for square in self._adjacent_squares(from_square)
                if self._is_on_board_square(square)]

    def _is_on_board_square(self, square):
        return 0 <= square[0] < self.n and 0 <= square[1] < self.n

    def _available_moves_from_square(self, from_square):
        return [(from_square, to_square) for to_square in self._adjacent_on_board_squares(from_square)
                if self.at(to_square) == 0]

    @classmethod
    def getCanonicalForm(cls, state, player):
        array = np.array([0] * 64)
        for square, unit in state.items():
            array[cls.canonical_form_index(square)] = unit.color
        return array

    @classmethod
    def canonical_form_index(cls, square):
        return square[0] * 8 + square[1]

