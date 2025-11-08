import Board from "./components/Board";

export default function App() {
  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-blue-500 via-sky-500 to-indigo-600 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-extrabold text-white drop-shadow-md mb-6">
        Chess 2.0
      </h1>
      <Board />
    </div>
  );
}