'''Start/goal spots: White start (1,1), black start (8,8)
White territory: (1,1) - (3,3) in a square, (2,7) - (1,8) in a square
'''

class Board:
    def __init__(self):
        # grid is a dict keyed by (row, col) -> piece or None
        self.grid = self._board_setup()
        # zones used for placement and special rules
        self.zones = self._mark_zones()

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

        # --- White territory main (1,1)-(3,3) -> 0-2,0-2 ---
        for r in range(0, 3):
            for c in range(0, 3):
                zones[(r, c)] = "white_territory"

        # --- Additional white zone (1,7)-(2,8) -> 0-1,6-7 ---
        for r in range(0, 2):
            for c in range(6, 8):
                zones[(r, c)] = "white_territory"

        # --- Black territory main (mirror) -> 5-7,5-7 ---
        for r in range(5, 8):
            for c in range(5, 8):
                zones[(r, c)] = "black_territory"

        # --- Black extra zone (mirror of white extra) bottom-left 2x2 -> 6-7,0-1 ---
        for r in range(6, 8):
            for c in range(0, 2):
                zones[(r, c)] = "black_territory"

        # --- Start/Goal spots ---
        zones[(0, 0)] = "white_start"
        zones[(7, 7)] = "black_start"

        return zones

    def get_piece(self, pos):
        return self.grid.get(pos)

    def place_piece(self, pos, piece, team):
        """Place a piece at pos if the team is allowed to place there.

        Returns True on success, False otherwise.
        """
        zone = self.zones.get(pos, "neutral")
        if team == "white" and (zone == "white_territory" or zone == "white_start"):
            self.grid[pos] = piece
            piece.position = pos
            return True
        if team == "black" and (zone == "black_territory" or zone == "black_start"):
            self.grid[pos] = piece
            piece.position = pos
            return True
        print("Invalid placement: outside your zone.")
        return False

    def move_piece(self, start, end):
        """Validate and perform move if legal for the piece."""
        piece = self.get_piece(start)
        if piece and end in piece.valid_moves(self):
            dest_piece = self.get_piece(end)

            # --- Special stacking logic for Calverymen ---
            if (
                getattr(piece, "is_calverymen", False)
                and dest_piece
                and getattr(dest_piece, "is_calverymen", False)
                and dest_piece.color == piece.color
            ):
                # Combine stack sizes, max 3
                src_stack = getattr(piece, "stack_size", 1)
                dest_stack = getattr(dest_piece, "stack_size", 1)
                new_stack = src_stack + dest_stack
                if new_stack > 3:
                    new_stack = 3  # cap at 3

                dest_piece.stack_size = new_stack

                # Remove the moving piece from its original square
                self.grid[start] = None
                # Destination Calverymen remains at `end` with updated stack_size
                return

            # --- Normal move / capture for all other cases ---
            self.grid[end] = piece
            self.grid[start] = None
            piece.position = end

    def check_winner(self):
        """
        Win condition:
        - White wins if a white piece reaches black's goal (7,7).
        - Black wins if a black piece reaches white's goal (0,0).
        Returns "white", "black", or None.
        """
        white_goal = (7, 7)
        black_goal = (0, 0)

        piece_at_white_goal = self.grid.get(white_goal)
        if piece_at_white_goal and piece_at_white_goal.color == "white":
            return "white"

        piece_at_black_goal = self.grid.get(black_goal)
        if piece_at_black_goal and piece_at_black_goal.color == "black":
            return "black"

        return None

    def to_dict(self):
        pieces = []
        for (row, col), piece in self.grid.items():
            if piece is not None:
                pieces.append(
                    {
                        "id": f"{piece.__class__.__name__}_{row}_{col}",
                        "type": piece.__class__.__name__,
                        "color": piece.color,
                        "row": row,
                        "col": col,
                    }
                )
        return {"pieces": pieces}
