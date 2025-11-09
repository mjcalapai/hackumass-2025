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

const getPieceLabel = (piece) => {
  return PIECE_SYMBOLS[piece.type] || "?";
};

const getPieceClasses = (piece) => {
  return piece.color === "white" ? "text-white" : "text-black";
};

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
  const [selected, setSelected] = useState(null);

  const handleClick = (r, c) => {
    setSelected([r, c]);
  };

  return (
    <div className="grid grid-cols-8 gap-1 bg-blue-900/50 p-3 rounded-2xl shadow-xl border border-blue-400/50">
      {Array.from({ length: SIZE }).map((_, r) =>
        Array.from({ length: SIZE }).map((_, c) => {
          const isSelected = selected && selected[0] === r && selected[1] === c;
          return (
            <div
              key={`${r}-${c}`}
              onClick={() => handleClick(r, c)}
              className={`w-14 h-14 flex items-center justify-center rounded-xl cursor-pointer transition-all
              ${isSelected ? "bg-yellow-400 scale-105" : (r + c) % 2 === 0 ? "bg-blue-700/80" : "bg-blue-800/80"}
              hover:brightness-110`}
            ></div>
          );
        })
      )}
    </div>
  );
}
