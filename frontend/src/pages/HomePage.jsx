import { useEffect, useState } from "react";

export default function HomePage() {
  const [randomPlayer, setRandomPlayer] = useState(null);
  const mockPlayers = [
    { name: "LeBron James", team: "Lakers" },
    { name: "Stephen Curry", team: "Warriors" },
    { name: "Kevin Durant", team: "Suns" },
    { name: "Giannis Antetokounmpo", team: "Bucks" },
  ];

  useEffect(() => {
    const random = mockPlayers[Math.floor(Math.random() * mockPlayers.length)];
    setRandomPlayer(random);
  }, []);

  const scrollTo = (id) => {
    const section = document.getElementById(id);
    if (section) {
      section.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Navbar */}
      <nav className="bg-gray-800 px-6 py-4 flex justify-between items-center shadow-md sticky top-0 z-50">
        <div className="text-2xl font-bold text-purple-400">PlayerGaugeAI</div>
        <div className="space-x-4">
          <button onClick={() => scrollTo("home")} className="hover:text-purple-300">Home</button>
          <button onClick={() => scrollTo("players")} className="hover:text-purple-300">Players</button>
          <button onClick={() => scrollTo("chat")} className="hover:text-purple-300">Chat</button>
          <button onClick={() => scrollTo("about")} className="hover:text-purple-300">About</button>
        </div>
      </nav>

      {/* Welcome Section */}
      <section id="home" className="p-10 text-center">
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

      {/* Players Section */}
      <section id="players" className="p-10 bg-gray-800 text-center">
        <h2 className="text-3xl font-bold text-purple-300 mb-4">Explore Players</h2>
        <p className="text-gray-400 mb-4">This section will include player stats, predictions, and search features.</p>
        {/* Placeholder content */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {mockPlayers.map((player, idx) => (
            <div key={idx} className="bg-gray-700 p-4 rounded shadow">
              <h3 className="text-lg text-purple-200">{player.name}</h3>
              <p className="text-sm text-gray-400">{player.team}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Chat Section */}
      <section id="chat" className="p-10 text-center">
        <h2 className="text-3xl font-bold text-purple-300 mb-4">AI Chat Assistant</h2>
        <p className="text-gray-400 mb-4">Ask anything about player stats, salaries, or predictions.</p>
        <div className="mx-auto max-w-xl bg-gray-800 p-6 rounded-lg">
          {/* Placeholder for chat UI */}
          <div className="text-gray-400">[Chat Interface Coming Soon]</div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="p-10 bg-gray-800 text-center">
        <h2 className="text-3xl font-bold text-purple-300 mb-4">About PlayerGaugeAI</h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          PlayerGaugeAI is a dashboard that uses machine learning to predict NBA salaries based on player performance.
          Designed with intuitive UX, real-time APIs, and scalable architecture.
        </p>
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
