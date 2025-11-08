from board import Board
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

    def _switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"