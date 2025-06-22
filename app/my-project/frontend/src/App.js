import { useState, useEffect } from 'react';
import logo from './logo.svg';

function App() {

  const [featuredPlayer, setFeaturedPlayer] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/featured-player')
      .then((res) => res.json())
      .then((data) => setFeaturedPlayer(data))
      .catch((err) => console.error("Error fetching player data:", err));
  }, []);

  return (
    <div className="font-titillium bg-blue-900 text-white pt-20">
      {/* Navbar */}
      <nav className="bg-blue-800 shadow-md fixed top-0 w-full z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <a href="#home" className="flex items-center">
            <img
              src={logo}
              alt="Logo"
              className="w-40 md:w-56 transition duration-300 hover:brightness-0 hover:invert hover:sepia hover:hue-rotate-[330deg] hover:saturate-[5] hover:contrast-[1.2]"
            />
          </a>



          <ul className="flex gap-6 text-white font-semibold">
            <li><a href="#home" className="hover:text-orange-400">Home</a></li>
            <li><a href="#players" className="hover:text-orange-400">Players</a></li>
            <li><a href="#teams" className="hover:text-orange-400">Teams</a></li>
            <li><a href="#analytics" className="hover:text-orange-400">Analytics</a></li>
            <li><a href="#about" className="hover:text-orange-400">About</a></li>
          </ul>
        </div>
      </nav>

      {/* Home Section */}
      <section id="home" className="min-h-screen flex flex-col items-center justify-center text-center px-6 bg-gradient-to-br from-blue-900 to-blue-700">
        <h1 className="text-5xl font-bold mb-4">AI-Powered NBA Player Evaluator</h1>
        <p className="text-lg text-blue-200 mb-6">Ask our chatbot to evaluate performance, salary fit, and player trends.</p>
        <div className="w-full max-w-xl bg-white text-black rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Ask the AI</h2>
          <textarea
            placeholder="What would be the fair salary for Tyrese Maxey's current performance?"
            className="w-full p-3 border border-gray-300 rounded-md mb-4 resize-none"
          ></textarea>
          <button className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 px-4 rounded">Send</button>
        </div>
      </section>

      {/* Players Section */}
      <section id="players" className="py-20 bg-blue-800 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-10">Player Evaluations</h2>

          {/* Featured Player Snapshot */}
          <div className="max-w-3xl mx-auto text-center mb-16">
            <h3 className="text-3xl font-semibold text-orange-400 mb-6">Today's Featured Player</h3>

            {featuredPlayer ? (
              <div className="bg-white text-black rounded-xl shadow-md p-6 text-left">
                <h4 className="text-2xl font-bold mb-2">{featuredPlayer.PLAYER_NAME}</h4>
                <ul className="text-sm mb-4">
                  <li><strong>Team:</strong> {featuredPlayer.TEAM_ABBREVIATION}</li>
                  <li><strong>PPG:</strong> {featuredPlayer.PPG}</li>
                  <li><strong>APG:</strong> {featuredPlayer.APG}</li>
                  <li><strong>RPG:</strong> {featuredPlayer.RPG}</li>
                  <li><strong>Age:</strong> {featuredPlayer.AGE}</li>
                </ul>
                <p className="text-base font-semibold text-orange-500">Estimated Salary: ${featuredPlayer.PREDICTED_SALARY}M</p>
                <p className="text-sm text-gray-700 mt-2">Based on recent performance and league trends.</p>
              </div>
            ) : (
              <p className="text-blue-200">Loading player data...</p>
            )}
          </div>


          {/* Feature Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-blue-700 p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <h3 className="text-xl font-semibold text-orange-400">Efficiency Ratings</h3>
              <p className="text-sm text-blue-200">Compare predicted salary to actual performance to spot undervalued players.</p>
            </div>
            <div className="bg-blue-700 p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <h3 className="text-xl font-semibold text-orange-400">Clustering Analysis</h3>
              <p className="text-sm text-blue-200">Group players by playstyle and metrics for role-based comparisons.</p>
            </div>
            <div className="bg-blue-700 p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <h3 className="text-xl font-semibold text-orange-400">Breakout Watch</h3>
              <p className="text-sm text-blue-200">Identify emerging talent based on year-over-year improvement trends.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Teams Section */}
      <section id="teams" className="py-20 bg-blue-900 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-10">Team Insights</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-blue-700 p-6 rounded-xl shadow-md">
              <h3 className="text-xl font-semibold text-orange-300">Top Team Value</h3>
              <p className="text-sm text-blue-200">See which teams are getting the most out of their payroll.</p>
            </div>
            <div className="bg-blue-700 p-6 rounded-xl shadow-md">
              <h3 className="text-xl font-semibold text-orange-300">Underperformers</h3>
              <p className="text-sm text-blue-200">Highlight teams with high spending but low ROI on court.</p>
            </div>
            <div className="bg-blue-700 p-6 rounded-xl shadow-md">
              <h3 className="text-xl font-semibold text-orange-300">Lineup Synergy</h3>
              <p className="text-sm text-blue-200">Evaluate which player combos yield the best results.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Analytics Section */}
      <section id="analytics" className="py-20 bg-gradient-to-br from-blue-800 to-blue-600 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Analytics Dashboard</h2>
          <p className="text-blue-100 mb-8">Explore player metrics, team dynamics, and salary prediction accuracy.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
            <div className="bg-white text-black p-6 rounded-xl shadow-lg">
              <h3 className="text-xl font-semibold mb-2">Model Insights</h3>
              <p className="text-sm">Understand which features contribute most to predicted salaries using explainable AI.</p>
            </div>
            <div className="bg-white text-black p-6 rounded-xl shadow-lg">
              <h3 className="text-xl font-semibold mb-2">Salary vs. Performance</h3>
              <p className="text-sm">Visualize how player performance aligns with compensation league-wide.</p>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-blue-950 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-orange-400 mb-4">About PlayerGaugeAI</h2>
          <p className="text-blue-200 text-lg mb-6">PlayerGaugeAI is an intelligent NBA analytics platform built to bridge the gap between machine learning and everyday fans. With tools for evaluating players and analyzing team dynamics, our mission is to make advanced insights accessible to all.</p>
          <ul className="text-blue-300 text-left max-w-2xl mx-auto list-disc pl-6">
            <li>AI-powered chatbot for personalized basketball insights</li>
            <li>Performance clustering and player comparison tools</li>
            <li>Visual analytics dashboards and salary evaluation</li>
            <li>Updated daily with real-world player performance data</li>
          </ul>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-blue-800 text-center py-6">
        <p className="text-blue-300">&copy; 2025 PlayerGaugeAI. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
