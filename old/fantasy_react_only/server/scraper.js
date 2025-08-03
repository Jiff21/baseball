const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class BaseballScraper {
  constructor() {
    this.dbPath = path.join(__dirname, 'fantasy_baseball.db');
    this.db = new sqlite3.Database(this.dbPath);
    this.baseUrl = 'https://www.mlb.com';
  }

  // Scrape player stats from MLB.com or similar source
  async scrapePlayerStats() {
    try {
      console.log('Starting player stats scraping...');
      
      // This is a simplified example - in reality you'd scrape from MLB.com or use their API
      // For now, we'll add some sample data to demonstrate the structure
      const samplePlayers = [
        {
          player_name: 'Mike Trout',
          team: 'LAA',
          position: 'OF',
          handedness: 'Righty',
          hits: 140,
          runs: 85,
          rbi: 95,
          home_runs: 35,
          stolen_bases: 8,
          walks: 90,
          strikeouts: 120,
          games_played: 140,
          at_bats: 520
        },
        {
          player_name: 'Ronald Acuna Jr.',
          team: 'ATL',
          position: 'OF',
          handedness: 'Righty',
          hits: 160,
          runs: 110,
          rbi: 85,
          home_runs: 40,
          stolen_bases: 35,
          walks: 75,
          strikeouts: 140,
          games_played: 150,
          at_bats: 580
        },
        {
          player_name: 'Juan Soto',
          team: 'SD',
          position: 'OF',
          handedness: 'Lefty',
          hits: 145,
          runs: 95,
          rbi: 100,
          home_runs: 30,
          stolen_bases: 12,
          walks: 110,
          strikeouts: 100,
          games_played: 145,
          at_bats: 500
        },
        {
          player_name: 'Mookie Betts',
          team: 'LAD',
          position: 'OF',
          handedness: 'Righty',
          hits: 155,
          runs: 105,
          rbi: 90,
          home_runs: 32,
          stolen_bases: 18,
          walks: 85,
          strikeouts: 110,
          games_played: 148,
          at_bats: 540
        },
        {
          player_name: 'Vladimir Guerrero Jr.',
          team: 'TOR',
          position: '1B',
          handedness: 'Righty',
          hits: 150,
          runs: 80,
          rbi: 110,
          home_runs: 38,
          stolen_bases: 2,
          walks: 70,
          strikeouts: 95,
          games_played: 145,
          at_bats: 550
        }
      ];

      for (const player of samplePlayers) {
        await this.savePlayerStats(player);
      }

      console.log('Player stats scraping completed!');
    } catch (error) {
      console.error('Error scraping player stats:', error);
    }
  }

  // Scrape team pitching stats
  async scrapeTeamStats() {
    try {
      console.log('Starting team stats scraping...');
      
      // Sample team pitching data
      const sampleTeams = [
        {
          team_name: 'Los Angeles Angels',
          vs_lefty_era: 4.25,
          vs_righty_era: 4.10,
          vs_lefty_whip: 1.35,
          vs_righty_whip: 1.28,
          runs_allowed_per_game: 4.8,
          hits_allowed_per_game: 8.5,
          home_runs_allowed_per_game: 1.2,
          walks_allowed_per_game: 3.2,
          strikeouts_per_game: 8.8
        },
        {
          team_name: 'Atlanta Braves',
          vs_lefty_era: 3.85,
          vs_righty_era: 3.70,
          vs_lefty_whip: 1.25,
          vs_righty_whip: 1.20,
          runs_allowed_per_game: 4.2,
          hits_allowed_per_game: 7.8,
          home_runs_allowed_per_game: 1.0,
          walks_allowed_per_game: 2.8,
          strikeouts_per_game: 9.5
        },
        {
          team_name: 'San Diego Padres',
          vs_lefty_era: 4.05,
          vs_righty_era: 3.95,
          vs_lefty_whip: 1.30,
          vs_righty_whip: 1.25,
          runs_allowed_per_game: 4.5,
          hits_allowed_per_game: 8.2,
          home_runs_allowed_per_game: 1.1,
          walks_allowed_per_game: 3.0,
          strikeouts_per_game: 9.2
        },
        {
          team_name: 'Los Angeles Dodgers',
          vs_lefty_era: 3.60,
          vs_righty_era: 3.45,
          vs_lefty_whip: 1.18,
          vs_righty_whip: 1.15,
          runs_allowed_per_game: 3.8,
          hits_allowed_per_game: 7.2,
          home_runs_allowed_per_game: 0.9,
          walks_allowed_per_game: 2.5,
          strikeouts_per_game: 10.1
        },
        {
          team_name: 'Toronto Blue Jays',
          vs_lefty_era: 4.15,
          vs_righty_era: 4.00,
          vs_lefty_whip: 1.32,
          vs_righty_whip: 1.27,
          runs_allowed_per_game: 4.6,
          hits_allowed_per_game: 8.3,
          home_runs_allowed_per_game: 1.3,
          walks_allowed_per_game: 3.1,
          strikeouts_per_game: 8.9
        }
      ];

      for (const team of sampleTeams) {
        await this.saveTeamStats(team);
      }

      console.log('Team stats scraping completed!');
    } catch (error) {
      console.error('Error scraping team stats:', error);
    }
  }

  // Save player stats to database
  savePlayerStats(playerData) {
    return new Promise((resolve, reject) => {
      const sql = `INSERT OR REPLACE INTO player_stats 
        (player_name, team, position, handedness, hits, runs, rbi, home_runs, 
         stolen_bases, walks, strikeouts, games_played, at_bats, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`;

      this.db.run(sql, [
        playerData.player_name,
        playerData.team,
        playerData.position,
        playerData.handedness,
        playerData.hits,
        playerData.runs,
        playerData.rbi,
        playerData.home_runs,
        playerData.stolen_bases,
        playerData.walks,
        playerData.strikeouts,
        playerData.games_played,
        playerData.at_bats
      ], function(err) {
        if (err) {
          console.error('Error saving player stats:', err);
          reject(err);
        } else {
          console.log(`Saved stats for ${playerData.player_name}`);
          resolve(this.lastID);
        }
      });
    });
  }

  // Save team stats to database
  saveTeamStats(teamData) {
    return new Promise((resolve, reject) => {
      const sql = `INSERT OR REPLACE INTO team_stats 
        (team_name, vs_lefty_era, vs_righty_era, vs_lefty_whip, vs_righty_whip,
         runs_allowed_per_game, hits_allowed_per_game, home_runs_allowed_per_game,
         walks_allowed_per_game, strikeouts_per_game, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`;

      this.db.run(sql, [
        teamData.team_name,
        teamData.vs_lefty_era,
        teamData.vs_righty_era,
        teamData.vs_lefty_whip,
        teamData.vs_righty_whip,
        teamData.runs_allowed_per_game,
        teamData.hits_allowed_per_game,
        teamData.home_runs_allowed_per_game,
        teamData.walks_allowed_per_game,
        teamData.strikeouts_per_game
      ], function(err) {
        if (err) {
          console.error('Error saving team stats:', err);
          reject(err);
        } else {
          console.log(`Saved stats for ${teamData.team_name}`);
          resolve(this.lastID);
        }
      });
    });
  }

  // Run full scraping process
  async runFullScrape() {
    console.log('Starting full scraping process...');
    await this.scrapePlayerStats();
    await this.scrapeTeamStats();
    console.log('Full scraping process completed!');
    this.close();
  }

  // Close database connection
  close() {
    this.db.close((err) => {
      if (err) {
        console.error('Error closing database:', err);
      } else {
        console.log('Database connection closed.');
      }
    });
  }
}

// Run scraper if called directly
if (require.main === module) {
  const scraper = new BaseballScraper();
  scraper.runFullScrape().catch(console.error);
}

module.exports = BaseballScraper;

