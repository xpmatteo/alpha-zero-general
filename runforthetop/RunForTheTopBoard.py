

class Board():
    """
    Author: Eric P. Nichols; modified by Matteo Vaccari
    Board data:
      1=white, -1=black, 0=empty
      first dim is row , 2nd is col:
         pieces[1][7] is the square in row 1, column 7
    Squares are stored and manipulated as (r,c) tuples.
    r is the row, c is the col.
    """

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n=8):
        """Set up initial board configuration."""
        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # Set up the initial 4 pieces.
        self.pieces[7][2] = 1
        self.pieces[7][3] = 1
        self.pieces[7][4] = -1
        self.pieces[7][5] = -1

    def __getitem__(self, index):
        """add [][] indexer syntax to the Board"""
        return self.pieces[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    count += 1
                if self[x][y]==-color:
                    count -= 1
        return count

    # public
    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for c in range(self.n):
            for r in range(self.n):
                if self[r][c] == color:
                    newmoves = self.get_moves_for_square((r,c))
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    newmoves = self.get_moves_for_square((x,y))
                    if len(newmoves)>0:
                        return True
        return False

    # --- private methods ---

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        (r,c) must be a valid square and must contain a piece of a given color.
        the available moves are all the orthogonal and diagonal squares,
        minus the squares occupied by pieces of the any color.
        """
        (r,c) = square

        # determine the color of the piece.
        color = self[r][c]

        # skip empty source squares.
        if color == 0:
            raise Exception("No piece at "+str(square))

        # search all possible directions.
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                # print(square,move,direction)
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        # print(move)
        flips = [flip for direction in self.__directions
                      for flip in self._get_flips(move, direction, color)]
        assert len(list(flips))>0
        for x, y in flips:
            #print(self[x][y],color)
            self[x][y] = color

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        color = self[x][y]
        flips = []

        for x, y in Board._increment_move(origin, direction, self.n):
            if self[x][y] == 0:
                if flips:
                    # print("Found", x,y)
                    return (x, y)
                else:
                    return None
            elif self[x][y] == color:
                return None
            elif self[x][y] == -color:
                # print("Flip",x,y)
                flips.append((x, y))

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        #initialize variables
        flips = [origin]

        for x, y in Board._increment_move(origin, direction, self.n):
            #print(x,y)
            if self[x][y] == 0:
                return []
            if self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == color and len(flips) > 0:
                #print(flips)
                return flips

        return []

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move=list(map(sum,zip(move,direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

    def _adjacent_squares(self, square):
        """ Returns the list of squares adjacent to the given square """
        return [self._add_square(square, direction) for direction in self.__directions]

    def _add_square(self, square, direction):
        return (square[0]+direction[0], square[1]+direction[1])

    def _adjacent_on_board_squares(self, square):
        return [square for square in self._adjacent_squares(square)
                if self._is_on_board_square(square)]

    def _is_on_board_square(self, square):
        return 0 <= square[0] < self.n and 0 <= square[1] < self.n

    def _available_moves_from_square(self, square):
        return [square for square in self._adjacent_on_board_squares(square)
                if self[square[0]][square[1]] == 0]
