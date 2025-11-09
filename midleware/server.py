from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core_components.game_state import GameState

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

game = GameState()  # single game instance for now

@app.get("/state")
def get_state():
    snapshot = {}
    for pos, piece in game.board.grid.items():
        if piece:
            snapshot[f"{pos[0]},{pos[1]}"] = {
                "type": piece.__class__.__name__,
                "color": piece.color,
            }
    return {"turn": game.turn, "board": snapshot}

@app.post("/move")
def make_move(start_row: int, start_col: int, end_row: int, end_col: int):
    ok = game.make_move((start_row, start_col), (end_row, end_col))
    return {"ok": ok}
