/**
 * Frontend fantasy baseball calculations utility
 */
import { ScoringSettings, ExpectedGameResult } from '../types';

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
    // Per-PA stats for more accurate calculations
    k_per_pa?: number;
    bb_per_pa?: number;
    hr_per_pa?: number;
    hits_per_pa?: number;
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
    // Per-PA stats for more accurate calculations
    k_per_pa?: number;
    bb_per_pa?: number;
    hr_per_pa?: number;
    hits_per_pa?: number;
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
    inning: number,
    scoringSettings: ScoringSettings
  ): ExpectedGameResult {
    // Select appropriate stats based on handedness
    const stats = handedness.toLowerCase() === 'lefty' ? teamStats.vs_lefty : teamStats.vs_righty;
    
    // Calculate PA per inning multiplier if data is available
    let paPerInning = 1.0; // Default multiplier
    if (teamStats.total_plate_appearances && teamStats.games_played) {
      // Formula: (Total plate appearances / games played) / 9
      paPerInning = (teamStats.total_plate_appearances / teamStats.games_played) / 9;
    }
    
    // Calculate expected stats per inning
    const inningsFactor = inning / 9.0;
    
    // Basic expected stats - use per-PA stats if available, otherwise fallback to per-9 stats
    const expectedHits = stats.hits_per_pa 
      ? (stats.hits_per_pa * (inningsFactor * paPerInning))
      : (stats.hits_per_9 * inningsFactor * paPerInning) / 9;
    
    const expectedWalks = stats.bb_per_pa
      ? (stats.bb_per_pa * (inningsFactor * paPerInning))
      : (stats.bb_per_9 * inningsFactor * paPerInning) / 9;
    
    const expectedStrikeouts = stats.k_per_pa
      ? (stats.k_per_pa * (inningsFactor * paPerInning))
      : (stats.k_per_9 * inningsFactor * paPerInning) / 9;
    
    const expectedHomeRuns = stats.hr_per_pa
      ? (stats.hr_per_pa * (inningsFactor * paPerInning))
      : (stats.hr_per_9 * inningsFactor * paPerInning) / 9;
    
    // ERA calculation remains the same (runs per inning, not per PA)
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
    
    // Break down hits into singles, doubles, triples
    // Typical distribution: ~75% singles, ~20% doubles, ~3% triples, ~2% HR
    const expectedSingles = expectedHits * 0.75;
    const expectedDoubles = expectedHits * 0.20;
    const expectedTriples = expectedHits * 0.03;
    
    // Calculate batting fantasy points
    const battingPoints = (
      expectedSingles * scoringSettings.batting.S +
      expectedDoubles * scoringSettings.batting.D +
      expectedTriples * scoringSettings.batting.T +
      expectedHomeRuns * scoringSettings.batting.HR +
      expectedWalks * scoringSettings.batting.BB +
      expectedRuns * scoringSettings.batting.R +
      expectedStrikeouts * scoringSettings.batting.SO
    );
    
    // For simplicity, assume RBI roughly equals runs
    const expectedRbi = expectedRuns;
    const totalBattingPoints = battingPoints + (expectedRbi * scoringSettings.batting.RBI);
    
    // Calculate pitching fantasy points
    // The innings value should be multiplied by the pitching-INN scoring setting
    const pitchingInningsPoints = inning * scoringSettings.pitching.INN;
    
    // Add other pitching stats (simplified calculation based on expected stats)
    const pitchingPoints = (
      pitchingInningsPoints +
      (expectedWalks * 9 * inningsFactor) * scoringSettings.pitching.BB + // Scale walks to full game
      (expectedRuns * 9 * inningsFactor) * scoringSettings.pitching.ER + // Scale earned runs
      (expectedHits * 9 * inningsFactor) * scoringSettings.pitching.HA + // Scale hits allowed
      (expectedHomeRuns * 9 * inningsFactor) * scoringSettings.pitching.HRA + // Scale HR allowed
      (expectedStrikeouts * 9 * inningsFactor) * scoringSettings.pitching.K + // Scale strikeouts
      winsPerGame * scoringSettings.pitching.W + // Wins per game
      lossesPerGame * scoringSettings.pitching.L // Losses per game
    );
    
    // Only use pitching points for fantasy calculation (batting removed per request)
    const totalFantasyPoints = pitchingPoints;
    
    return {
      team_abbreviation: teamStats.abbreviation,
      handedness,
      inning,
      expected_fantasy_points: Math.round(totalFantasyPoints * 100) / 100,
      batting_points: Math.round(totalBattingPoints * 100) / 100,
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
    inning: number,
    scoringSettings: ScoringSettings
  ): ExpectedGameResult[] {
    return allTeamStats.map(teamStats => 
      this.calculateTeamExpectedPoints(teamStats, handedness, inning, scoringSettings)
    );
  }

  /**
   * Add color coding based on percentiles for visualization
   */
  static addColorCoding(results: ExpectedGameResult[]): ExpectedGameResult[] {
    if (results.length === 0) return [];

    const points = results.map(r => r.expected_fantasy_points);
    const minPoints = Math.min(...points);
    const maxPoints = Math.max(...points);

    return results.map(result => {
      const pointsValue = result.expected_fantasy_points;
      
      let colorScore: number;
      let colorCategory: 'excellent' | 'good' | 'average' | 'poor';

      if (maxPoints === minPoints) {
        // All teams have same expected points
        colorScore = 0.5;
        colorCategory = 'average';
      } else {
        // Normalize to 0-1 scale
        colorScore = (pointsValue - minPoints) / (maxPoints - minPoints);
        
        // Categorize
        if (colorScore >= 0.7) {
          colorCategory = 'excellent';
        } else if (colorScore >= 0.5) {
          colorCategory = 'good';
        } else if (colorScore >= 0.3) {
          colorCategory = 'average';
        } else {
          colorCategory = 'poor';
        }
      }

      return {
        ...result,
        color_score: colorScore,
        color_category: colorCategory
      };
    });
  }
}
