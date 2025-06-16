export default function HomePage() {
  const scrollTo = (id) => {
    const section = document.getElementById(id);
    if (section) {
      section.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white pt-20">
      {/* Navbar */}
      <nav className="bg-gray-800 px-6 py-4 flex justify-between items-center shadow-md fixed top-0 w-full z-50">
        {/* PlayerGaugeAI as Home button on left */}
        <div
          onClick={() => scrollTo("home")}
          className="text-2xl font-bold text-purple-400 cursor-pointer select-none"
          aria-label="Go to Home"
          role="button"
          tabIndex={0}
          onKeyPress={(e) => { if (e.key === 'Enter') scrollTo("home") }}
        >
          PlayerGaugeAI
        </div>

        {/* Navigation links */}
        <div className="space-x-6">
          <button onClick={() => scrollTo("players")} className="hover:text-purple-300">
            Players
          </button>
          <button onClick={() => scrollTo("chat")} className="hover:text-purple-300">
            Chat
          </button>
          <button onClick={() => scrollTo("about")} className="hover:text-purple-300">
            About
          </button>
        </div>
      </nav>

      {/* Sections with tighter spacing and max-width containers */}
      <section id="home" className="py-10">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-4xl font-bold text-purple-300 mb-2">Welcome to PlayerGaugeAI</h1>
          <p className="text-gray-300">
            An intelligent platform for exploring NBA player performance through machine learning.
          </p>
        </div>
      </section>

      <section id="players" className="py-10 bg-gray-800">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-purple-300 mb-2">Explore Players</h2>
          <p className="text-gray-400">
            This section will include player stats, predictions, and search features.
          </p>
        </div>
      </section>

      <section id="chat" className="py-10">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-purple-300 mb-2">AI Chat Assistant</h2>
          <p className="text-gray-400 mb-2">
            Ask anything about player stats, salaries, or predictions.
          </p>
          <div className="bg-gray-800 p-6 rounded-lg">
            <div className="text-gray-400">[Chat Interface Coming Soon]</div>
          </div>
        </div>
      </section>

      <section id="about" className="py-10 bg-gray-800">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-purple-300 mb-2">About PlayerGaugeAI</h2>
          <p className="text-gray-400">
            PlayerGaugeAI is a dashboard that uses machine learning to predict NBA salaries based on player performance.
            Designed with intuitive UX, real-time APIs, and scalable architecture.
          </p>
        </div>
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
