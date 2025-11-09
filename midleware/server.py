from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core_components.game_state import GameState
from core_components.pieces import (
    Slinger,
    Chariott,
    Plumbata,
    Ballista,
    Straight,
    ThrustingSpearman,
    ArcherFootSoldier,
    Calverymen,
    BatteringRam,
    Francisca,
    Diplomat,
    SeigeTower,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = GameState()  # single game instance


def setup_initial_positions():
    # -------- WHITE PIECES (13 total) --------
    # Top-left 3x3 (9 squares)
    white_placements = [
        ((0, 0), Slinger("white", (0, 0))),
        ((0, 1), Plumbata("white", (0, 1))),
        ((0, 2), Ballista("white", (0, 2))),

        ((1, 0), ThrustingSpearman("white", (1, 0))),
        ((1, 1), ArcherFootSoldier("white", (1, 1))),
        ((1, 2), BatteringRam("white", (1, 2))),

        ((2, 0), Francisca("white", (2, 0))),
        ((2, 1), Diplomat("white", (2, 1))),
        ((2, 2), SeigeTower("white", (2, 2))),
    ]

    # Top-right 2x2 staging (4 squares): 1x Chariott, 3x Calverymen
    white_placements += [
        ((0, 6), Chariott("white", (0, 6))),
        ((0, 7), Calverymen("white", (0, 7))),
        ((1, 6), Calverymen("white", (1, 6))),
        ((1, 7), Calverymen("white", (1, 7))),
    ]
    # 9 + 4 = 13

    # -------- BLACK PIECES (13 total, mirrored) --------
    # Bottom-right 3x3 (9 squares)
    black_placements = [
        ((7, 7), Slinger("black", (7, 7))),
        ((7, 6), Plumbata("black", (7, 6))),
        ((7, 5), Ballista("black", (7, 5))),

        ((6, 7), ThrustingSpearman("black", (6, 7))),
        ((6, 6), ArcherFootSoldier("black", (6, 6))),
        ((6, 5), BatteringRam("black", (6, 5))),

        ((5, 7), Francisca("black", (5, 7))),
        ((5, 6), Diplomat("black", (5, 6))),
        ((5, 5), SeigeTower("black", (5, 5))),
    ]

    # Bottom-left 2x2 staging (mirror of white top-right)
    black_placements += [
        ((7, 0), Chariott("black", (7, 0))),
        ((7, 1), Calverymen("black", (7, 1))),
        ((6, 0), Calverymen("black", (6, 0))),
        ((6, 1), Calverymen("black", (6, 1))),
    ]
    # 9 + 4 = 13

    # -------- Apply placements --------
    for pos, piece in white_placements:
        ok = game.place_piece(pos, piece, "white")
        if not ok:
            print(f"[WARN] Failed to place WHITE {piece.__class__.__name__} at {pos}")

    for pos, piece in black_placements:
        ok = game.place_piece(pos, piece, "black")
        if not ok:
            print(f"[WARN] Failed to place BLACK {piece.__class__.__name__} at {pos}")

    piece_count = len(game.board.to_dict()["pieces"])
    print(f"[INIT] Placed {piece_count} pieces on the board.")


class MoveRequest(BaseModel):
    start_row: int
    start_col: int
    end_row: int
    end_col: int


@app.get("/api/board")
def get_board():
    return game.board.to_dict()


@app.post("/api/move")
def make_move(move: MoveRequest):
    ok = game.make_move(
        (move.start_row, move.start_col),
        (move.end_row, move.end_col),
    )
    return {
        "ok": ok,
        "board": game.board.to_dict(),
        "turn": game.turn,
        "winner": game.winner,
    }


# Run setup when module is imported
setup_initial_positions()
