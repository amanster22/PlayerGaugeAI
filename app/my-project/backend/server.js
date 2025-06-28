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
  const query = `SELECT * FROM player_data ORDER BY RANDOM() LIMIT 1`;
  db.get(query, [], (err, row) => {
    if (err) {
      console.error("❌ Error fetching random player:", err.message);
      return res.status(500).json({ error: "Failed to fetch random player" });
    }
    res.json(row);
  });
});

const PORT = 5001;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
