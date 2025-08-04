/**
 * Frontend fantasy baseball calculations utility
 */
import { ScoringSettings, FantasyExpectedStartScore } from '../types';

export interface TeamStats {
  abbreviation: string;
  name: string;
  // Optional plate appearances data for PA per inning calculation
  total_plate_appearances?: number;
  games_played?: number;
  vs_lefty: {
    era: number;
    whip: number;
    k_per_9: number;
    bb_per_9: number;
    hr_per_9: number;
    hits_per_9: number;
    wins?: number;
    losses?: number;
  };
  vs_righty: {
    era: number;
    whip: number;
    k_per_9: number;
    bb_per_9: number;
    hr_per_9: number;
    hits_per_9: number;
    wins?: number;
    losses?: number;
  };
}

export class FantasyCalculations {
  /**
   * Calculate expected fantasy points for a single team
   */
  static calculateTeamExpectedPoints(
    teamStats: TeamStats,
    handedness: 'Lefty' | 'Righty',
    expectedInnings: number,
    scoringSettings: ScoringSettings
  ): FantasyExpectedStartScore {
    // Select appropriate stats based on handedness
    const stats = handedness.toLowerCase() === 'lefty' ? teamStats.vs_lefty : teamStats.vs_righty;
    
    // Calculate PA per inning multiplier if data is available
    let paPerInning = 1.0; // Default multiplier
    if (teamStats.total_plate_appearances && teamStats.games_played) {
      // Formula: (Total plate appearances / games played) / 9
      paPerInning = (teamStats.total_plate_appearances / teamStats.games_played) / 9;
    }
    
    // Calculate expected stats per inning using expectedInnings (from form)
    const inningsFactor = expectedInnings / 9.0;
    
    // Basic expected stats (simplified calculation) - all multiplied by expectedInnings
    const expectedHits = (stats.hits_per_9 * inningsFactor);
    const expectedWalks = (stats.bb_per_9 * inningsFactor);
    const expectedStrikeouts = (stats.k_per_9 * inningsFactor);
    const expectedHomeRuns = (stats.hr_per_9 * inningsFactor);
    const expectedRuns = (stats.era * inningsFactor);
    
    // Calculate wins and losses per game if data is available
    let winsPerGame = 0;
    let lossesPerGame = 0;
    if (stats.wins !== undefined && stats.losses !== undefined) {
      const totalGames = stats.wins + stats.losses;
      if (totalGames > 0) {
        winsPerGame = stats.wins / totalGames;
        lossesPerGame = stats.losses / totalGames;
      }
    }
    
    // Break down hits into singles, doubles, triples for display purposes only
    // Typical distribution: ~75% singles, ~20% doubles, ~3% triples, ~2% HR
    const expectedSingles = expectedHits * 0.75;
    const expectedDoubles = expectedHits * 0.20;
    const expectedTriples = expectedHits * 0.03;
    
    // For display purposes, assume RBI roughly equals runs
    const expectedRbi = expectedRuns;
    
    // Calculate pitching fantasy points
    // Pitching points = expectedInnings * innings (from sidebar scoring settings)
    const pitchingInningsPoints = expectedInnings * scoringSettings.pitching.INN;
    
    // Add other pitching stats (scaled properly for expected innings)
    const pitchingPoints = (
      pitchingInningsPoints +
      expectedWalks * scoringSettings.pitching.BB + // Walks for expected innings
      expectedRuns * scoringSettings.pitching.ER + // Earned runs for expected innings  
      expectedHits * scoringSettings.pitching.HA + // Hits allowed for expected innings
      expectedHomeRuns * scoringSettings.pitching.HRA + // HR allowed for expected innings
      expectedStrikeouts * scoringSettings.pitching.K + // Strikeouts for expected innings
      (winsPerGame * expectedInnings / 9) * scoringSettings.pitching.W + // Wins scaled for expected innings
      (lossesPerGame * expectedInnings / 9) * scoringSettings.pitching.L // Losses scaled for expected innings
    );
    
    // Only use pitching points for fantasy calculation (batting removed per request)
    const totalFantasyPoints = pitchingPoints;
    
    return {
      team_abbreviation: teamStats.abbreviation,
      handedness,
      inning: expectedInnings,
      expected_fantasy_points: Math.round(totalFantasyPoints * 100) / 100,
      batting_points: 0, // Batting calculations removed per request
      pitching_points: Math.round(pitchingPoints * 100) / 100,
      pa_per_inning: Math.round(paPerInning * 1000) / 1000, // PA per I
      expected_runs: Math.round(expectedRuns * 1000) / 1000,
      expected_hits: Math.round(expectedHits * 1000) / 1000,
      expected_singles: Math.round(expectedSingles * 1000) / 1000,
      expected_doubles: Math.round(expectedDoubles * 1000) / 1000,
      expected_triples: Math.round(expectedTriples * 1000) / 1000,
      expected_home_runs: Math.round(expectedHomeRuns * 1000) / 1000,
      expected_walks: Math.round(expectedWalks * 1000) / 1000,
      expected_strikeouts: Math.round(expectedStrikeouts * 1000) / 1000,
      expected_rbi: Math.round(expectedRbi * 1000) / 1000,
      expected_wins: Math.round(winsPerGame * 1000) / 1000,
      expected_losses: Math.round(lossesPerGame * 1000) / 1000,
      team_stats: stats
    };
  }

  /**
   * Calculate expected fantasy points for all teams
   */
  static calculateAllTeamsExpectedPoints(
    allTeamStats: TeamStats[],
    handedness: 'Lefty' | 'Righty',
    expectedInnings: number,
    scoringSettings: ScoringSettings
  ): FantasyExpectedStartScore[] {
    return allTeamStats.map(teamStats => 
      this.calculateTeamExpectedPoints(teamStats, handedness, expectedInnings, scoringSettings)
    );
  }

  /**
   * Add color coding based on standard deviations for visualization
   */
  static addColorCoding(results: FantasyExpectedStartScore[]): FantasyExpectedStartScore[] {
    if (results.length === 0) return [];

    const points = results.map(r => r.expected_fantasy_points);
    
    // Calculate mean and standard deviation
    const mean = points.reduce((sum, p) => sum + p, 0) / points.length;
    const variance = points.reduce((sum, p) => sum + Math.pow(p - mean, 2), 0) / points.length;
    const standardDeviation = Math.sqrt(variance);

    return results.map(result => {
      const pointsValue = result.expected_fantasy_points;
      
      let colorScore: number;
      let colorCategory: 'good' | 'average' | 'bad';

      // Calculate how many standard deviations from mean
      const deviationsFromMean = (pointsValue - mean) / standardDeviation;
      
      if (deviationsFromMean >= 2.0) {
        // Two standard deviations above average = Good (Green)
        colorCategory = 'good';
        colorScore = 1.0;
      } else if (deviationsFromMean <= -2.0) {
        // Two standard deviations below average = Bad (Red)
        colorCategory = 'bad';
        colorScore = 0.0;
      } else {
        // Within two standard deviations = Average (No color)
        colorCategory = 'average';
        colorScore = 0.5;
      }

      return {
        ...result,
        color_score: colorScore,
        color_category: colorCategory
      };
    });
  }
}
