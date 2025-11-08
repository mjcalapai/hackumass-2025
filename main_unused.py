# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from core_components.game_state import GameState
# from core_components.pieces import (
#     Slinger, Chariott, Plumbata, Ballista, Straight,
#     ThrustingSpearman, ArcherFootSoldier, Calverymen,
#     BatteringRam, Francisca, Diplomat, Prince, SeigeTower,
# )

# app = FastAPI()

# # allow frontend dev server
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# game_state = GameState()


# def setup_initial_positions():
#     # Same logic as your test_moves.py setup_all_pieces
#     placements = [
#         ((0, 0), Slinger("white", (0, 0))),
#         ((0, 1), Straight("white", (0, 1))),
#         ((0, 2), Ballista("white", (0, 2))),
#         ((1, 0), Plumbata("white", (1, 0))),
#         ((1, 1), ThrustingSpearman("white", (1, 1))),
#         ((1, 2), ArcherFootSoldier("white", (1, 2))),
#         ((2, 0), BatteringRam("white", (2, 0))),
#         ((2, 1), Francisca("white", (2, 1))),
#         ((2, 2), Diplomat("white", (2, 2))),
#         ((0, 6), SeigeTower("white", (0, 6))),
#         ((0, 7), Prince("white", (0, 7))),
#         ((1, 6), Chariott("white", (1, 6))),
#         ((1, 7), Calverymen("white", (1, 7))),
#     ]

#     for pos, piece in placements:
#         game_state.place_piece(pos, piece, "white")


# # Initialize once on startup
# setup_initial_positions()


# @app.get("/api/board")
# def get_board():
#     return game_state.board.to_dict()
