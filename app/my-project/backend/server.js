// const express = require('express');
// const cors = require('cors');
// const bodyParser = require('body-parser');
// const sqlite3 = require('sqlite3').verbose(); // or pg for PostgreSQL
// const path = require('path');

// const app = express();
// const db = new sqlite3.Database('./nba.db'); // or use PG connection

// app.use(cors());
// app.use(bodyParser.json());

// app.post('/api/query', (req, res) => {
//   const { query } = req.body;
//   db.all(query, [], (err, rows) => {
//     if (err) {
//       console.error("DB error:", err);
//       return res.json({ error: err.message });
//     }
//     res.json({ results: rows });
//   });
// });

// app.listen(5000, () => console.log("Server running on http://localhost:5000"));
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

app.use(cors());
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

const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running on http://localhost:${PORT}`));
