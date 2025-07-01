const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();

// ✅ Use absolute path to avoid "no such table" errors
// const dbPath = path.resolve(__dirname, 'nba_data.db');
// const dbPath = path.resolve(__dirname, 'nba_dataV2.db');
const dbPath = path.resolve(__dirname, 'nba_dataV3.db');

const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error('❌ Failed to connect to database:', err.message);
  } else {
    console.log('✅ Connected to nba_dataV3.db');
  }
});

const dbGet = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) {
        console.error("❌ dbGet error:", err);
        reject(err);
      } else {
        console.log("dbGet result row:", row);
        resolve(row);
      }
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


app.get("/api/featured-player", async (req, res) => {
  try {
    const query = `
      SELECT *, 
             SALARY_CONDENSED AS FORMATTED_SALARY,
             ROUND(PREDICTED_SALARY, 2) AS FORMATTED_PREDICTED_SALARY
      FROM player_data
      ORDER BY RANDOM()
      LIMIT 1;
    `;

    const row = await dbGet(query);  // <-- Use dbGet here
    res.json(row);
  } catch (err) {
    console.error("Error fetching featured player:", err);
    res.status(500).json({ error: "Database error" });
  }
});


app.get("/api/player-lookup", async (req, res) => {
  const name = req.query.name?.trim();
  console.log(`🔍 Player lookup requested for name: "${name}"`);

  if (!name) {
    console.log("❌ Missing name parameter in request");
    return res.json({ error: "Missing name" });
  }

  try {
    const query = `
      SELECT *,
             SALARY_CONDENSED AS FORMATTED_SALARY,
             ROUND(PREDICTED_SALARY, 2) AS FORMATTED_PREDICTED_SALARY,
             ROUND(SALARY_PCT_CHANGE, 2) AS SALARY_PCT_CHANGE
      FROM player_data
      WHERE LOWER(PLAYER_NAME) LIKE LOWER(?)
      LIMIT 1;
    `;

    const row = await dbGet(query, [`%${name}%`]);  // <-- Use dbGet here

    if (!row) {
      console.log(`⚠️ No player found matching: "${name}"`);
      return res.json({ error: "Player not found" });
    }

    console.log("✅ Player found:", row);
    res.json({ player: row });

  } catch (err) {
    console.error("❌ Lookup error:", err);
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
  SALARY_CONDENSED AS FORMATTED_SALARY,
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
    }, 0);

    const roundedTeamSalary = parseFloat(teamSalaryMil.toFixed(2));

    res.json({ players, teamSalary: roundedTeamSalary });

  } catch (err) {
    console.error("❌ DB error:", err.message);
    res.status(500).json({ error: "Failed to fetch team players" });
  }
});






const PORT = 5001;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
