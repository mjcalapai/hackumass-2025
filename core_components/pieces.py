DIRECTIONS = {
    "orthogonal": [(1,0), (-1,0), (0,1), (0,-1)],
    "diagonal": [(1,1), (1,-1), (-1,1), (-1,-1)],
    "king": [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
}

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def _explore_dir(self, board, dr, dc, max_range=8):
        r, c = self.position
        moves = []
        for step in range(1, max_range + 1):
            nr, nc = r + dr*step, c + dc*step
            if not in_bounds(nr, nc):
                break
            target = board.grid.get((nr, nc))
            if target is None:
                moves.append((nr, nc))
            elif target.color != self.color:
                moves.append((nr, nc))
                break
            else:
                break
        return moves

    def valid_moves(self, board, rng=8):
        raise NotImplementedError


class Slinger(Piece):
    def valid_moves(self, board, rng=8):
        moves = []
        for dr, dc in DIRECTIONS["orthogonal"] + DIRECTIONS["diagonal"]:
            moves += self._explore_dir(board, dr, dc, rng)
        return moves


class Chariott(Piece):
    def valid_moves(self, board, rng=8):
        moves = []
        for dr, dc in DIRECTIONS["orthogonal"] + DIRECTIONS["diagonal"]:
            for step in range(1, rng + 1):
                nr, nc = self.position[0] + dr*step, self.position[1] + dc*step
                if not in_bounds(nr, nc):
                    break
                target = board.grid.get((nr, nc))
                if target is not None and target.color != self.color:
                    moves.append((nr, nc))
                    break
                elif target is not None:
                    break
        return moves


class Plumbata(Piece):
    def valid_moves(self, board, rng=8):
        moves = []
        for dr, dc in DIRECTIONS["orthogonal"] + DIRECTIONS["diagonal"]:
            moves += self._explore_dir(board, dr, dc, rng)
        return moves


class Ballista(Piece):
    def valid_moves(self, board, rng=8):
        moves = []
        for dr, dc in DIRECTIONS["orthogonal"]:
            moves += self._explore_dir(board, dr, dc, rng)
        return moves


class Straight(Piece):
    def valid_moves(self, board, rng=8):
        moves = []
        for dr, dc in DIRECTIONS["orthogonal"]:
            moves += self._explore_dir(board, dr, dc, rng)
        return moves


class ThrustingSpearman(Piece):
    def valid_moves(self, board, rng=1):
        moves = []
        for dr, dc in DIRECTIONS["king"]:
            nr, nc = self.position[0] + dr, self.position[1] + dc
            if in_bounds(nr, nc):
                target = board.grid.get((nr, nc))
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves


class ArcherFootSoldier(Piece):
    def valid_moves(self, board, rng=8):
        moves = []
        for dr, dc in DIRECTIONS["diagonal"]:
            moves += self._explore_dir(board, dr, dc, rng)
        return moves


class Calverymen(Piece):
    def __init__(self, color, position, stack_size=1):
        super().__init__(color, position)
        self.stack_size = max(1, min(stack_size, 3))
        self.is_calverymen = True

    def _max_range(self):
        size = max(1, min(self.stack_size, 3))
        if size == 1:
            return 1
        if size == 2:
            return 3
        return 6

    def valid_moves(self, board, rng=None):
        max_range = self._max_range()
        moves = []

        for dr, dc in DIRECTIONS["king"]:
            for step in range(1, max_range + 1):
                nr = self.position[0] + dr * step
                nc = self.position[1] + dc * step
                if not in_bounds(nr, nc):
                    break

                target = board.grid.get((nr, nc))
                if target is None:
                    moves.append((nr, nc))
                else:
                    if getattr(target, "is_calverymen", False) and target.color == self.color:
                        moves.append((nr, nc))  # stack
                    elif target.color != self.color:
                        moves.append((nr, nc))  # capture
                    break

        return moves


class BatteringRam(Piece):
    def valid_moves(self, board, rng=1):
        moves = []
        for dr, dc in DIRECTIONS["diagonal"]:
            nr, nc = self.position[0] + dr, self.position[1] + dc
            if in_bounds(nr, nc):
                target = board.grid.get((nr, nc))
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves


class Francisca(Piece):
    def valid_moves(self, board, rng=1):
        moves = []
        for dr, dc in DIRECTIONS["king"]:
            nr, nc = self.position[0] + dr, self.position[1] + dc
            if in_bounds(nr, nc):
                target = board.grid.get((nr, nc))
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves


class Diplomat(Piece):
    def valid_moves(self, board, rng=1):
        moves = []
        for dr, dc in DIRECTIONS["king"]:
            nr, nc = self.position[0] + dr, self.position[1] + dc
            if in_bounds(nr, nc):
                target = board.grid.get((nr, nc))
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves


class Prince(Piece):
    def valid_moves(self, board, rng=1):
        return []


class SeigeTower(Piece):
    def valid_moves(self, board, rng=1):
        moves = []
        for dr, dc in DIRECTIONS["king"]:
            nr, nc = self.position[0] + dr, self.position[1] + dc
            if not in_bounds(nr, nc):
                continue
            zone = board.zones.get((nr, nc), "neutral")
            target = board.grid.get((nr, nc))

            if target is None:
                moves.append((nr, nc))
            elif target.color != self.color and "territory" in zone:
                moves.append((nr, nc))
        return moves
