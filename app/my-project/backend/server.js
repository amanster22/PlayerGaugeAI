const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
app.use(cors());

// Connect to SQLite database file
const db = new sqlite3.Database('./nba_data.db');

// API endpoint example
app.get('/api/featured-player', (req, res) => {
  const sql = `SELECT PLAYER_NAME, TEAM_ABBREVIATION, PPG, APG, RPG, AGE, PREDICTED_SALARY FROM player_data ORDER BY RANDOM() LIMIT 1`;
  db.get(sql, [], (err, row) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(row);
  });
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
