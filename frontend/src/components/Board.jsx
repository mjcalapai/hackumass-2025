import { useEffect, useState } from "react";

const SIZE = 8;

// Map Python class names -> placeholder letters shown on the board
const PIECE_SYMBOLS = {
  Slinger: "Sl",
  Chariott: "Ch",
  Plumbata: "P",
  Ballista: "B",
  Straight: "St",
  ThrustingSpearman: "Ts",
  ArcherFootSoldier: "A",
  Calverymen: "H",
  BatteringRam: "Br",
  Francisca: "F",
  Diplomat: "D",
  Prince: "Pr",
  SeigeTower: "T", // or "ST"
};

export default function Board() {
  const [selected, setSelected] = useState(null);
  const [pieces, setPieces] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/board")
      .then((res) => res.json())
      .then((data) => {
        setPieces(data.pieces || []);
      })
      .catch((err) => {
        console.error("Failed to load board", err);
      });
  }, []);

  const getPieceAt = (row, col) =>
    pieces.find((p) => p.row === row && p.col === col);

  const handleClick = (row, col) => {
    setSelected({ row, col });
  };

  return (
    <div className="grid grid-cols-8 gap-1 bg-blue-900/50 p-3 rounded-2xl shadow-xl border border-blue-400/50">
      {Array.from({ length: SIZE }).map((_, row) =>
        Array.from({ length: SIZE }).map((_, col) => {
          const isSelected =
            selected && selected.row === row && selected.col === col;
          const piece = getPieceAt(row, col);

          return (
            <div
              key={`${row}-${col}`}
              onClick={() => handleClick(row, col)}
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
                <span className="text-white font-extrabold text-xs text-center leading-tight select-none">
                  {PIECE_SYMBOLS[piece.type] || "?"}
                </span>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}
