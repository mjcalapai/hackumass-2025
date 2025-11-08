from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core_components.game_state import GameState
from core_components.pieces import (
    Slinger, Chariott, Plumbata, Ballista, Straight,
    ThrustingSpearman, ArcherFootSoldier, Calverymen,
    BatteringRam, Francisca, Diplomat, Prince, SeigeTower,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

game = GameState()  # single game instance


def setup_initial_positions():
    # -------- WHITE PIECES (top / left zones) --------
    white_placements = [
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

    # -------- BLACK PIECES (bottom-right black_territory) --------
    # All coords are within (5..7, 5..7) or (7,7) which matches black_territory / black_start.
    black_placements = [
        ((7, 7), Slinger("black", (7, 7))),
        ((7, 6), Straight("black", (7, 6))),
        ((7, 5), Ballista("black", (7, 5))),
        ((6, 7), Plumbata("black", (6, 7))),
        ((6, 6), ThrustingSpearman("black", (6, 6))),
        ((6, 5), ArcherFootSoldier("black", (6, 5))),
        ((5, 7), BatteringRam("black", (5, 7))),
        ((5, 6), Francisca("black", (5, 6))),
        ((5, 5), Diplomat("black", (5, 5))),
        ((7, 5), SeigeTower("black", (7, 5))),
        # If you want a black "Prince" & mounted units down here too:
        ((5, 5), Prince("black", (5, 5))),        # adjust if you want unique spot
        ((5, 6), Chariott("black", (5, 6))),
        ((5, 7), Calverymen("black", (5, 7))),
    ]

    # because I reused some squares in this quick sketch, let's keep it simple & safe:
    # better: comment the extras and only place unique coords:
    black_placements = [
        ((7, 7), Slinger("black", (7, 7))),
        ((7, 6), Straight("black", (7, 6))),
        ((7, 5), Ballista("black", (7, 5))),
        ((6, 7), Plumbata("black", (6, 7))),
        ((6, 6), ThrustingSpearman("black", (6, 6))),
        ((6, 5), ArcherFootSoldier("black", (6, 5))),
        ((5, 7), BatteringRam("black", (5, 7))),
        ((5, 6), Francisca("black", (5, 6))),
        ((5, 5), Diplomat("black", (5, 5))),
        ((7, 5), SeigeTower("black", (7, 5))),
        ((5, 5), Prince("black", (5, 5))),  # if conflict, move later
        # you can tweak exact layout later based on rules
    ]

    # Place all
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


setup_initial_positions()


@app.get("/api/board")
def get_board():
    return game.board.to_dict()


class MoveRequest(BaseModel):
    start_row: int
    start_col: int
    end_row: int
    end_col: int


@app.post("/api/move")
def make_move(move: MoveRequest):
    ok = game.make_move(
        (move.start_row, move.start_col),
        (move.end_row, move.end_col),
    )
    # Always return current board + whose turn, even if move failed
    return {
        "ok": ok,
        "board": game.board.to_dict(),
        "turn": game.turn,
    }
