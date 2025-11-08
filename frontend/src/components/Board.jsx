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

export default function Board() {
  const [selected, setSelected] = useState(null); // { row, col } or null
  const [pieces, setPieces] = useState([]);
  const [turn, setTurn] = useState("white");
  const [message, setMessage] = useState("");

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
          // Successful move -> update board from backend
          setPieces(data.board.pieces || []);
          setTurn(data.turn);
          setMessage("");
        } else {
          // Illegal move (backend rejected)
          setMessage("Illegal move");
        }
        setSelected(null);
      })
      .catch((err) => {
        console.error("Move failed", err);
        setMessage("Move request failed");
        setSelected(null);
      });
  };

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="text-white text-sm">
        Turn: <span className="font-bold capitalize">{turn}</span>
      </div>
      {message && (
        <div className="text-yellow-300 text-xs h-4">{message}</div>
      )}
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
                  <span className="text-white font-extrabold text-[10px] text-center leading-tight select-none">
                    {PIECE_SYMBOLS[piece.type] || "?"}
                  </span>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
