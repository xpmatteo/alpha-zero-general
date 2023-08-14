import numpy as np

class Board():
    """
    Author: Eric P. Nichols; modified by Matteo Vaccari
    Board data:
      1=white, -1=black, 0=empty
      first dim is row , 2nd is col:
         pieces[1][7] is the square in row 1, column 7
    Squares are stored and manipulated as (r,c) tuples,
    where r is the row, c is the col.
    Moves are pairs of the form (from_square, to_square).
    """

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n=8):
        """Set up initial board configuration."""
        self.n = n
        self.HALF_BOARD_SIZE = n//2
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # Set up the initial 4 pieces.
        self.pieces[7][2] = 1
        self.pieces[7][3] = 1
        self.pieces[7][4] = -1
        self.pieces[7][5] = -1

    @classmethod
    def fromState(cls, state):
        board = Board()
        board.pieces = state
        return board

    @classmethod
    def cloneState(cls, state):
        board = Board()
        board.pieces = np.copy(state)
        return board

    def __getitem__(self, index):
        """add [][] indexer syntax to the Board"""
        return self.pieces[index]

    def at(self, square):
        """ get square color from a pair (r,c) """
        return self[square[0]][square[1]]

    def set(self, square, color):
        """ set color of square (r,c)"""
        self[square[0]][square[1]] = color

    # public
    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        1 for white O, -1 for black X
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for c in range(self.n):
            for r in range(self.n):
                if self[r][c] == color:
                    newmoves = self._available_moves_from_square((r,c))
                    moves.update(newmoves)
        return list(moves)

    # public
    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    newmoves = self.get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    def execute_move(self, move):
        from_square, to_square = move
        color = self.at(from_square)
        if color == 0:
            raise ValueError("No piece at from_square")
        self.set(to_square, color)
        self.set(from_square, 0)

    # --- private methods ---

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

    def game_status(self):
        player1 = 0
        player_minus1 = 0
        for r in range(0, self.HALF_BOARD_SIZE):
            for c in range(self.n):
                if self[r][c] == 1:
                    player1 += 1
                elif self[r][c] == -1:
                    player_minus1 += 1
        if player1 == 2:
            return 1
        elif player_minus1 == 2:
            return -1
        else:
            return 0

    def state(self):
        return np.array(self.pieces)

