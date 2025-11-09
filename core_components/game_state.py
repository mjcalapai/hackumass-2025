from core_components.board import Board


class GameState:
    def __init__(self):
        self.board = Board()
        self.turn = "white"
        self.move_history = []
        self.winner = None

    def make_move(self, start, end):
        if self.winner is not None:
            return False

        piece = self.board.get_piece(start)
        if piece and piece.color == self.turn:
            if end in piece.valid_moves(self.board):
                self.board.move_piece(start, end)
                self.move_history.append((start, end))

                winner = self.board.check_winner()
                if winner:
                    self.winner = winner
                    return True

                self._switch_turn()
                return True

        return False

    def _switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

    def place_piece(self, pos, piece, team):
        return self.board.place_piece(pos, piece, team)

    def get_piece(self, pos):
        return self.board.get_piece(pos)

    def get_board_state(self):
        snapshot = {}
        for pos, piece in self.board.grid.items():
            if piece:
                snapshot[pos] = {
                    "type": piece.__class__.__name__,
                    "color": piece.color,
                }
        return snapshot
