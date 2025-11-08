# test_moves.py

from core_components.game_state import GameState
from core_components.pieces import (
    Slinger, Chariott, Plumbata, Ballista, Straight,
    ThrustingSpearman, ArcherFootSoldier, Calverymen,
    BatteringRam, Francisca, Diplomat, Prince, SeigeTower,
)

def setup_all_pieces():
    gs = GameState()

    # All positions are inside white_territory or white_start/extra zone
    placements = [
        ((0, 0), Slinger("white", (0, 0))),
        ((0, 1), Straight("white", (0, 1))),
        ((0, 2), Ballista("white", (0, 2))),
        ((1, 0), Plumbata("white", (1, 0))),
        ((1, 1), ThrustingSpearman("white", (1, 1))),
        ((1, 2), ArcherFootSoldier("white", (1, 2))),
        ((2, 0), BatteringRam("white", (2, 0))),
        ((2, 1), Francisca("white", (2, 1))),
        ((2, 2), Diplomat("white", (2, 2))),
        ((0, 6), SeigeTower("white", (0, 6))),
        ((0, 7), Prince("white", (0, 7))),
        ((1, 6), Chariott("white", (1, 6))),
        ((1, 7), Calverymen("white", (1, 7))),
    ]

    for pos, piece in placements:
        ok = gs.place_piece(pos, piece, "white")
        if not ok:
            print(f"[WARN] Failed to place {piece.__class__.__name__} at {pos}")

    return gs


def print_board(board):
    """Quick ASCII view: first letter of piece class or '.' for empty."""
    for r in range(8):
        row = ""
        for c in range(8):
            p = board.grid[(r, c)]
            row += (p.__class__.__name__[0] if p else ".") + " "
        print(row)
    print()


def run_smoke_test():
    gs = setup_all_pieces()
    print("Initial turn (expected 'white'):", gs.turn)
    print("\nInitial board:")
    print_board(gs.board)

    # ===== VALID MOVE =====
    # ArcherFootSoldier moves diagonally: (1,2) -> (2,3) is clear & legal.
    print("Test 1: VALID move ArcherFootSoldier (1,2) -> (2,3)")
    moved_valid = gs.make_move((1, 2), (2, 3))
    print("Result (expected True):", moved_valid)
    print("Turn after move (expected 'black'):", gs.turn)
    print_board(gs.board)

    # ===== INVALID MOVE =====
    # Now it's black's turn, but we have only white pieces.
    # Trying to move Slinger should fail due to turn check.
    print("Test 2: INVALID move Slinger (0,0) -> (0,3) on black's turn")
    moved_invalid = gs.make_move((0, 0), (0, 3))
    print("Result (expected False):", moved_invalid)
    print("Turn should still be 'black':", gs.turn)
    print_board(gs.board)


if __name__ == "__main__":
    run_smoke_test()
