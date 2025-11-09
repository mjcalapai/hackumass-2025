import { useEffect, useState } from "react";

const SIZE = 8;

const PIECE_SYMBOLS = {
  Slinger: "Sl",
  Chariott: "Ch",
  Plumbata: "Pl",
  Ballista: "Ba",
  Straight: "St",
  ThrustingSpearman: "Ts",
  ArcherFootSoldier: "Af",
  Calverymen: "Cv",
  BatteringRam: "Br",
  Francisca: "Fr",
  Diplomat: "Dp",
  Prince: "Pr",
  SeigeTower: "T",
};

const getPieceLabel = (piece) => PIECE_SYMBOLS[piece.type] || "?";

const getPieceClasses = (piece) =>
  piece.color === "white" ? "text-white" : "text-black";

export default function Board() {
  const [selected, setSelected] = useState(null); // { row, col } or null
  const [pieces, setPieces] = useState([]);
  const [turn, setTurn] = useState("white");
  const [message, setMessage] = useState("");
  const [winner, setWinner] = useState(null);
  const [showRules, setShowRules] = useState(false);

  // Load initial board
  useEffect(() => {
    fetch("http://localhost:8000/api/board")
      .then((res) => res.json())
      .then((data) => {
        console.log("BOARD DATA FROM API:", data);
        setPieces(data.pieces || []);
      })
      .catch((err) => {
        console.error("Failed to load board", err);
        setMessage("Failed to load board");
      });
  }, []);

  const getPieceAt = (row, col) =>
    pieces.find((p) => p.row === row && p.col === col);

  const handleSquareClick = (row, col) => {
    // If game is over, ignore clicks
    if (winner) return;

    const clickedPiece = getPieceAt(row, col);

    // If no selection yet:
    if (!selected) {
      if (clickedPiece) {
        setSelected({ row, col });
        setMessage("");
      }
      return;
    }

    // If clicking same square -> deselect
    if (selected.row === row && selected.col === col) {
      setSelected(null);
      setMessage("");
      return;
    }

    // Otherwise: try to move from selected -> (row,col)
    const movePayload = {
      start_row: selected.row,
      start_col: selected.col,
      end_row: row,
      end_col: col,
    };

    fetch("http://localhost:8000/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(movePayload),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("MOVE RESULT:", data);

        if (data.ok) {
          setPieces(data.board.pieces || []);
          setTurn(data.turn);

          if (data.winner) {
            setWinner(data.winner);
            setMessage(`Game over: ${data.winner.toUpperCase()} wins!`);
          } else {
            setMessage("");
          }
        } else {
          if (data.winner) {
            setWinner(data.winner);
            setMessage(`Game over: ${data.winner.toUpperCase()} wins!`);
          } else {
            setMessage("Illegal move");
          }
        }

        setSelected(null);
      })
      .catch((err) => {
        console.error("Move request failed", err);
        setMessage("Move request failed");
        setSelected(null);
      });
  };

  return (
    <div className="flex flex-col items-center gap-3 relative">
      {/* Top bar: Turn / Winner + Help Icon */}
      <div className="flex items-center gap-3 w-full justify-center">
        <div className="text-white text-sm">
          {winner ? (
            <>
              Winner:{" "}
              <span className="font-bold capitalize">{winner}</span>
            </>
          ) : (
            <>
              Turn:{" "}
              <span className="font-bold capitalize">{turn}</span>
            </>
          )}
        </div>

        <button
          onClick={() => setShowRules(true)}
          className="ml-4 w-6 h-6 flex items-center justify-center rounded-full bg-white/90 text-blue-700 text-sm font-bold shadow hover:scale-105 transition"
          title="Show rules"
        >
          ?
        </button>
      </div>

      {message && (
        <div className="text-yellow-300 text-xs h-4">{message}</div>
      )}

      {/* Board */}
      <div className="grid grid-cols-8 gap-1 bg-blue-900/50 p-3 rounded-2xl shadow-xl border border-blue-400/50">
        {Array.from({ length: SIZE }).map((_, row) =>
          Array.from({ length: SIZE }).map((_, col) => {
            const isSelected =
              selected && selected.row === row && selected.col === col;
            const piece = getPieceAt(row, col);

            return (
              <div
                key={`${row}-${col}`}
                onClick={() => handleSquareClick(row, col)}
                className={`
                  w-14 h-14 flex items-center justify-center rounded-xl cursor-pointer transition-all
                  ${
                    isSelected
                      ? "bg-yellow-400 scale-105"
                      : (row + col) % 2 === 0
                      ? "bg-blue-700/80"
                      : "bg-blue-800/80"
                  }
                  hover:brightness-110
                `}
              >
                {piece && (
                  <span
                    className={`${getPieceClasses(
                      piece
                    )} font-extrabold text-[10px] text-center leading-tight select-none`}
                  >
                    {getPieceLabel(piece)}
                  </span>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Rules Modal */}
      {showRules && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white max-w-xl max-h-[80vh] w-full mx-4 rounded-2xl shadow-2xl p-5 overflow-y-auto relative">
            <button
              onClick={() => setShowRules(false)}
              className="absolute top-2 right-3 text-gray-500 hover:text-black text-xl leading-none"
            >
              ×
            </button>
            <h2 className="text-2xl font-extrabold mb-2 text-blue-700">
              BattleBoard Rules
            </h2>
            <p className="text-sm text-gray-800 mb-3">
              Objective: move one of your pieces onto the enemy&apos;s goal square.
              White wins by reaching <b>(7,7)</b>. Black wins by reaching <b>(0,0)</b>.
              Turns alternate between White and Black after every legal move.
            </p>

            <h3 className="text-lg font-bold mt-3 mb-1 text-blue-600">
              Board & Setup
            </h3>
            <ul className="list-disc list-inside text-sm text-gray-800 mb-3 space-y-1">
              <li>Each player starts with <b>13 pieces</b>.</li>
              <li>
                Each piece is shown as a short code (e.g. <b>Sl</b>, <b>Cv</b>).
                White letters are white, Black letters are black.
              </li>
              <li>
                Territory & staging zones restrict where pieces may be placed at start,
                but movement is validated by the server rules.
              </li>
            </ul>

            <h3 className="text-lg font-bold mt-3 mb-1 text-blue-600">
              Pieces & Codes
            </h3>
            <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-gray-900 mb-2">
              <div>
                <b>Sl</b> – Slinger:
                <div>Moves any distance in all 8 directions.</div>
              </div>
              <div>
                <b>Ch</b> – Chariott:
                <div>Line-based attacker; cannot pass through allies. Can only move if taking a piece of the 
                  other color.
                </div>
              </div>
              <div>
                <b>Pl</b> – Plumbata:
                <div>Ranged moves like Slinger (orthogonal+diagonal).</div>
              </div>
              <div>
                <b>Ba</b> – Ballista:
                <div>Straight lines (orthogonal only).</div>
              </div>
              <div>
                <b>St</b> – Straight:
                <div>Orthogonal movement piece.</div>
              </div>
              <div>
                <b>Ts</b> – ThrustingSpearman:
                <div>King-style, 1 square in any direction.</div>
              </div>
              <div>
                <b>Af</b> – ArcherFootSoldier:
                <div>Diagonals at range.</div>
              </div>
              <div>
                <b>Cv</b> – Calverymen:
                <div>
                  1 stacked: range 1.
                  <br />
                  2 stacked: range 3.
                  <br />
                  3 stacked: range 6.
                  <br />
                  Only stack on same-color Cv; no unstack.
                </div>
              </div>
              <div>
                <b>Br</b> – BatteringRam:
                <div>1 diagonal step (adjacent).</div>
              </div>
              <div>
                <b>Fr</b> – Francisca:
                <div>1 step any direction.</div>
              </div>
              <div>
                <b>Dp</b> – Diplomat:
                <div>1 step any direction.</div>
              </div>
              <div>
                <b>T</b> – SeigeTower:
                <div>
                  King-like movement; special attack rules in territories.
                </div>
              </div>
            </div>

            <p className="text-[11px] text-gray-600 mt-2">
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
