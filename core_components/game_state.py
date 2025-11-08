from core_components.board import Board


class GameState:
    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.move_history = []

    def make_move(self, start, end):
        piece = self.board.get_piece(start)
        if piece and piece.color == self.turn:
            if end in piece.valid_moves(self.board):
                self.board.move_piece(start, end)
                self.move_history.append((start, end))
                self._switch_turn()
                return True
        return False
    
    

    def _switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def place_piece(self, pos, piece, team):
        """Delegate piece placement rules to the Board implementation."""
        return self.board.place_piece(pos, piece, team)
    
    def get_piece(self, pos):
        return self.board.get_piece(pos)

    def get_board_state(self):
        """Return a simple snapshot for rendering."""
        snapshot = {}
        for pos, piece in self.board.grid.items():
            if piece:
                snapshot[pos] = {
                    "type": piece.__class__.__name__,
                    "color": piece.color,
                }
        return snapshot