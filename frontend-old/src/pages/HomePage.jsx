import { useEffect, useState } from "react";

export default function HomePage() {
  const [randomPlayer, setRandomPlayer] = useState(null);

  // Sample mock data — replace with backend/API call later
  const mockPlayers = [
    { name: "LeBron James", team: "Lakers" },
    { name: "Stephen Curry", team: "Warriors" },
    { name: "Kevin Durant", team: "Suns" },
    { name: "Giannis Antetokounmpo", team: "Bucks" }
  ];

  useEffect(() => {
    const random = mockPlayers[Math.floor(Math.random() * mockPlayers.length)];
    setRandomPlayer(random);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Navbar */}
      <nav className="bg-gray-800 px-6 py-4 flex justify-between items-center shadow-md">
        <div className="text-2xl font-bold text-purple-400">PlayerGaugeAI</div>
        <div className="space-x-4">
          <a href="#" className="hover:text-purple-300">Home</a>
          <a href="#" className="hover:text-purple-300">Players</a>
          <a href="#" className="hover:text-purple-300">Chat</a>
          <a href="#" className="hover:text-purple-300">About</a>
        </div>
      </nav>

      {/* Welcome Section */}
      <section className="p-10 text-center">
        <h1 className="text-4xl font-bold text-purple-300 mb-4">Welcome to PlayerGaugeAI</h1>
        <p className="text-gray-300 mb-8">
          An intelligent platform for exploring NBA player performance through machine learning.
        </p>

        {randomPlayer && (
          <div className="bg-gray-800 rounded-lg p-6 max-w-md mx-auto shadow-lg">
            <h2 className="text-xl font-semibold mb-2">Featured Player</h2>
            <p className="text-purple-200 text-lg">{randomPlayer.name}</p>
            <p className="text-sm text-gray-400">{randomPlayer.team}</p>
          </div>
        )}
      </section>

      {/* Chatbot Button */}
      <div className="fixed bottom-5 right-5">
        <button className="bg-purple-600 hover:bg-purple-700 text-white font-medium px-4 py-2 rounded-full shadow-lg">
          💬 Chatbot
        </button>
      </div>
    </div>
  );
}
