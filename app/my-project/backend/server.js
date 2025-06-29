const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();

// ✅ Use absolute path to avoid "no such table" errors
const dbPath = path.resolve(__dirname, 'nba_data.db');
const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error('❌ Failed to connect to database:', err.message);
  } else {
    console.log('✅ Connected to nba_data.db');
  }
});

const dbGet = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
};

app.use(cors({
  origin: 'http://localhost:3000',
  methods: ['GET', 'POST'],
  credentials: true
}));

app.use(bodyParser.json());

// ✅ SQL execution endpoint
app.post('/api/query', (req, res) => {
  const { query } = req.body;

  console.log('📥 SQL Query Received:', query);

  db.all(query, [], (err, rows) => {
    if (err) {
      console.error("❌ DB error:", err);
      return res.status(400).json({ error: `SQL Error: ${err.message}` });
    }
    res.json({ results: rows });
  });
});

// ✅ Optional: Test route to list tables
app.get('/api/test', (req, res) => {
  db.all("SELECT name FROM sqlite_master WHERE type='table'", [], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ tables: rows });
  });
});

// Random featured player endpoint
app.get('/api/featured-player', (req, res) => {
  const query = `SELECT PLAYER_NAME, TEAM_ABBREVIATION, AGE, PPG, APG, RPG, printf('%,.2f', PREDICTED_SALARY / 1000000.0) AS FORMATTED_SALARY, SALARY_PCT_CHANGE FROM player_data ORDER BY RANDOM() LIMIT 1`;
  db.get(query, [], (err, row) => {
    if (err) {
      console.error("❌ Error fetching random player:", err.message);
      return res.status(500).json({ error: "Failed to fetch random player" });
    }
    res.json(row);
  });
});

app.get("/api/player-lookup", async (req, res) => {
  const name = req.query.name?.toLowerCase();
  if (!name) return res.status(400).json({ error: "Missing player name" });

  try {
    const query = `
      SELECT PLAYER_NAME, TEAM_ABBREVIATION, AGE, PPG, APG, RPG, printf('%,.2f', PREDICTED_SALARY / 1000000.0) AS FORMATTED_SALARY, SALARY_PCT_CHANGE
      FROM player_data
      WHERE LOWER(PLAYER_NAME) LIKE ?
      LIMIT 1;
    `;

    const player = await dbGet(query, [`%${name}%`]);

    if (!player) return res.status(404).json({ error: "Player not found." });

    // 🔍 Add performance label based on SALARY_PCT_CHANGE
    const change = player.SALARY_PCT_CHANGE;

    if (change == null) {
      player.performance = "error";
    } else if (change > 5) {
      player.performance = "up";
    } else if (change < -5) {
      player.performance = "down";
    } else {
      player.performance = "middle";
    }

    res.json({ player });

  } catch (err) {
    console.error("❌ DB error:", err.message);
    res.status(500).json({ error: "Database error" });
  }
});

app.get('/api/team-players', async (req, res) => {
  const team = req.query.team?.toUpperCase();
  if (!team) return res.status(400).json({ error: "Missing team abbreviation" });

  const query = `
    SELECT 
      PLAYER_NAME, 
      PPG, 
      APG, 
      RPG, 
      printf('%,.2f', PREDICTED_SALARY / 1000000.0) AS FORMATTED_SALARY,
      ROUND(SALARY_PCT_CHANGE, 2) AS SALARY_PCT_CHANGE,
      PREDICTED_SALARY
    FROM player_data
    WHERE TEAM_ABBREVIATION = ?
    ORDER BY PREDICTED_SALARY DESC
    LIMIT 13;
  `;

  try {
    const players = await new Promise((resolve, reject) => {
      db.all(query, [team], (err, result) => {
        if (err) reject(err);
        else resolve(result);
      });
    });

    // Calculate team salary sum (in millions, rounded to 2 decimals)
    const teamSalaryMil = players.reduce((sum, player) => {
      return sum + (player.PREDICTED_SALARY || 0);
    }, 0) / 1_000_000;

    const roundedTeamSalary = parseFloat(teamSalaryMil.toFixed(2));

    res.json({ players, teamSalary: roundedTeamSalary });

  } catch (err) {
    console.error("❌ DB error:", err.message);
    res.status(500).json({ error: "Failed to fetch team players" });
  }
});






const PORT = 5001;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
