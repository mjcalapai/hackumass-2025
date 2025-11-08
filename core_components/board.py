'''Start/goal spots: White start (1,1), black start (8,8)
White territory: (1,1) - (3,3) in a square, (2,7) - (1,8) in a square

'''

class Board:
    def __init__(self):
        self.grid = self._board_setup()
    
    def _board_setup(self):
        #initialize a grid 8x8
        #tic tac toe logic with dictionary and pieces?
        board = {}
        #blank board, users picks
        for row in range(8):
            for col in range(8):
                board[(row, col)] = None
        return(board)
    

    def _board_setup(self):
        board = {}
        for row in range(8):
            for col in range(8):
                board[(row, col)] = None
        return board

    def _mark_zones(self):
        zones = {}
        for r in range(8):
            for c in range(8):
                zones[(r, c)] = "neutral"  # default

        # --- White territory (1,1)-(3,3) ---
        for r in range(0, 3):
            for c in range(0, 3):
                zones[(r, c)] = "white_territory"

        # --- Additional white zone (1,7)-(2,8) human coords -> (0-1,6-7) ---
        for r in range(0, 2):
            for c in range(6, 8):
                zones[(r, c)] = "white_territory"

        # --- Black territory (mirror example) ---
        for r in range(5, 8):
            for c in range(5, 8):
                zones[(r, c)] = "black_territory"

        # --- Start/Goal spots ---
        zones[(0, 0)] = "white_start"
        zones[(7, 7)] = "black_start"

        return zones



    def move_piece(self, start, end):
        # Validate and perform move
        
        piece = self.get_piece(start) #TODO get_piece()
        if piece and end in piece.valid_moves(self):
            self.grid[end] = piece
            self.grid[start] = None
            piece.position = end

    def check_winner(self):
        #easy condition, just check if another color piece is in the win square
        pass
