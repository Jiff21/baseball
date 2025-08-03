const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Database setup
const dbPath = path.join(__dirname, 'fantasy_baseball.db');
const db = new sqlite3.Database(dbPath);

// Initialize database tables
db.serialize(() => {
  // Player stats table
  db.run(`CREATE TABLE IF NOT EXISTS player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    team TEXT,
    position TEXT,
    handedness TEXT,
    hits REAL DEFAULT 0,
    runs REAL DEFAULT 0,
    rbi REAL DEFAULT 0,
    home_runs REAL DEFAULT 0,
    stolen_bases REAL DEFAULT 0,
    walks REAL DEFAULT 0,
    strikeouts REAL DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    at_bats INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Expected game calculations table
  db.run(`CREATE TABLE IF NOT EXISTS expected_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    handedness TEXT,
    league_type TEXT,
    scoring_settings TEXT, -- JSON string of scoring settings
    expected_hits REAL,
    expected_runs REAL,
    expected_rbi REAL,
    expected_home_runs REAL,
    expected_stolen_bases REAL,
    expected_walks REAL,
    expected_strikeouts REAL,
    expected_fantasy_points REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  // Team stats table for opponent analysis
  db.run(`CREATE TABLE IF NOT EXISTS team_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    vs_lefty_era REAL,
    vs_righty_era REAL,
    vs_lefty_whip REAL,
    vs_righty_whip REAL,
    runs_allowed_per_game REAL,
    hits_allowed_per_game REAL,
    home_runs_allowed_per_game REAL,
    walks_allowed_per_game REAL,
    strikeouts_per_game REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
});

// API Routes

// Get all players
app.get('/api/players', (req, res) => {
  db.all('SELECT * FROM player_stats ORDER BY player_name', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows);
  });
});

// Get player by name
app.get('/api/players/:name', (req, res) => {
  const playerName = req.params.name;
  db.get('SELECT * FROM player_stats WHERE player_name = ?', [playerName], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    if (!row) {
      res.status(404).json({ error: 'Player not found' });
      return;
    }
    res.json(row);
  });
});

// Add or update player stats
app.post('/api/players', (req, res) => {
  const {
    player_name,
    team,
    position,
    handedness,
    hits,
    runs,
    rbi,
    home_runs,
    stolen_bases,
    walks,
    strikeouts,
    games_played,
    at_bats
  } = req.body;

  const sql = `INSERT OR REPLACE INTO player_stats 
    (player_name, team, position, handedness, hits, runs, rbi, home_runs, 
     stolen_bases, walks, strikeouts, games_played, at_bats, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`;

  db.run(sql, [
    player_name, team, position, handedness, hits, runs, rbi, home_runs,
    stolen_bases, walks, strikeouts, games_played, at_bats
  ], function(err) {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ id: this.lastID, message: 'Player stats saved successfully' });
  });
});

// Calculate expected game performance
app.post('/api/calculate-expected', (req, res) => {
  const { player_name, handedness, league_type, scoring_settings } = req.body;

  // Get player stats
  db.get('SELECT * FROM player_stats WHERE player_name = ?', [player_name], (err, player) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    
    if (!player) {
      res.status(404).json({ error: 'Player not found' });
      return;
    }

    // Calculate expected stats per game (simplified calculation)
    const gamesPlayed = player.games_played || 1;
    const expectedStats = {
      expected_hits: (player.hits / gamesPlayed).toFixed(3),
      expected_runs: (player.runs / gamesPlayed).toFixed(3),
      expected_rbi: (player.rbi / gamesPlayed).toFixed(3),
      expected_home_runs: (player.home_runs / gamesPlayed).toFixed(3),
      expected_stolen_bases: (player.stolen_bases / gamesPlayed).toFixed(3),
      expected_walks: (player.walks / gamesPlayed).toFixed(3),
      expected_strikeouts: (player.strikeouts / gamesPlayed).toFixed(3)
    };

    // Calculate fantasy points based on scoring settings
    const fantasyPoints = (
      (expectedStats.expected_hits * scoring_settings.hits) +
      (expectedStats.expected_runs * scoring_settings.runs) +
      (expectedStats.expected_rbi * scoring_settings.rbi) +
      (expectedStats.expected_home_runs * scoring_settings.homeRuns) +
      (expectedStats.expected_stolen_bases * scoring_settings.stolenBases) +
      (expectedStats.expected_walks * scoring_settings.walks) +
      (expectedStats.expected_strikeouts * scoring_settings.strikeouts)
    ).toFixed(2);

    expectedStats.expected_fantasy_points = fantasyPoints;

    // Save calculation to database
    const saveSql = `INSERT INTO expected_games 
      (player_name, handedness, league_type, scoring_settings, expected_hits, 
       expected_runs, expected_rbi, expected_home_runs, expected_stolen_bases, 
       expected_walks, expected_strikeouts, expected_fantasy_points)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

    db.run(saveSql, [
      player_name, handedness, league_type, JSON.stringify(scoring_settings),
      expectedStats.expected_hits, expectedStats.expected_runs, expectedStats.expected_rbi,
      expectedStats.expected_home_runs, expectedStats.expected_stolen_bases,
      expectedStats.expected_walks, expectedStats.expected_strikeouts,
      expectedStats.expected_fantasy_points
    ], function(err) {
      if (err) {
        console.error('Error saving calculation:', err);
      }
    });

    res.json({
      player: player.player_name,
      ...expectedStats
    });
  });
});

// Get team stats
app.get('/api/teams', (req, res) => {
  db.all('SELECT * FROM team_stats ORDER BY team_name', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows);
  });
});

// Add or update team stats
app.post('/api/teams', (req, res) => {
  const {
    team_name,
    vs_lefty_era,
    vs_righty_era,
    vs_lefty_whip,
    vs_righty_whip,
    runs_allowed_per_game,
    hits_allowed_per_game,
    home_runs_allowed_per_game,
    walks_allowed_per_game,
    strikeouts_per_game
  } = req.body;

  const sql = `INSERT OR REPLACE INTO team_stats 
    (team_name, vs_lefty_era, vs_righty_era, vs_lefty_whip, vs_righty_whip,
     runs_allowed_per_game, hits_allowed_per_game, home_runs_allowed_per_game,
     walks_allowed_per_game, strikeouts_per_game, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`;

  db.run(sql, [
    team_name, vs_lefty_era, vs_righty_era, vs_lefty_whip, vs_righty_whip,
    runs_allowed_per_game, hits_allowed_per_game, home_runs_allowed_per_game,
    walks_allowed_per_game, strikeouts_per_game
  ], function(err) {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ id: this.lastID, message: 'Team stats saved successfully' });
  });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Fantasy Baseball API is running' });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Database connection closed.');
    process.exit(0);
  });
});

