import http.client
import json
import sqlite3

# --- Step 1: Fetch data from API ---
conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "98413bbceamsh26fdf527c4e4f94p10f0a3jsn43a7cd2ae075",
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

game_id = 8131  # Example game ID
conn.request("GET", f"/players/statistics?game={game_id}", headers=headers)
res = conn.getresponse()
data = res.read()

# Parse JSON
json_data = json.loads(data.decode("utf-8"))
player_stats = json_data.get("response", [])

# --- Step 2: Set up SQLite DB ---
db_conn = sqlite3.connect("nba_stats.db")
cursor = db_conn.cursor()

# Create table with full stat structure
cursor.execute("""
CREATE TABLE IF NOT EXISTS player_game_stats (
    game_id INTEGER,
    player_id INTEGER,
    firstname TEXT,
    lastname TEXT,
    team TEXT,
    position TEXT,
    minutes TEXT,
    points INTEGER,
    fgm INTEGER,
    fga INTEGER,
    fgp REAL,
    ftm INTEGER,
    fta INTEGER,
    ftp REAL,
    tpm INTEGER,
    tpa INTEGER,
    tpp REAL,
    off_reb INTEGER,
    def_reb INTEGER,
    total_reb INTEGER,
    assists INTEGER,
    steals INTEGER,
    turnovers INTEGER,
    fouls INTEGER
)
""")

# --- Step 3: Insert records safely ---
for player in player_stats:
    player_info = player.get("player", {})
    team_info = player.get("team", {})
    game_info = player.get("game", {})

    # Extract and parse all fields with default values
    cursor.execute("""
    INSERT INTO player_game_stats (
        game_id, player_id, firstname, lastname, team, position, minutes,
        points, fgm, fga, fgp,
        ftm, fta, ftp,
        tpm, tpa, tpp,
        off_reb, def_reb, total_reb,
        assists, steals, turnovers, fouls
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        game_info.get("id"),
        player_info.get("id"),
        player_info.get("firstname"),
        player_info.get("lastname"),
        team_info.get("name"),
        player.get("pos"),
        player.get("min"),
        player.get("points", 0),
        player.get("fgm", 0),
        player.get("fga", 0),
        float(player.get("fgp", "0").replace('%', '')) if player.get("fgp") else 0.0,
        player.get("ftm", 0),
        player.get("fta", 0),
        float(player.get("ftp", "0").replace('%', '')) if player.get("ftp") else 0.0,
        player.get("tpm", 0),
        player.get("tpa", 0),
        float(player.get("tpp", "0").replace('%', '')) if player.get("tpp") else 0.0,
        player.get("offReb", 0),
        player.get("defReb", 0),
        player.get("totReb", 0),
        player.get("assists", 0),
        player.get("steals", 0),
        player.get("turnovers", 0),  # Might be typo'd in your sample: "turn,"
        player.get("pFouls", 0)
    ))

# --- Step 4: Save and close ---
db_conn.commit()
db_conn.close()

print("✅ Full player game stats saved to nba_stats.db")
