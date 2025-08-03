/**
 * Frontend fantasy baseball calculations utility
 */
import { ScoringSettings, ExpectedGameResult } from '../types';

export interface TeamStats {
  abbreviation: string;
  name: string;
  vs_lefty: {
    era: number;
    whip: number;
    k_per_9: number;
    bb_per_9: number;
    hr_per_9: number;
    hits_per_9: number;
  };
  vs_righty: {
    era: number;
    whip: number;
    k_per_9: number;
    bb_per_9: number;
    hr_per_9: number;
    hits_per_9: number;
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
    
    // Calculate expected stats per inning
    const inningsFactor = inning / 9.0;
    
    // Basic expected stats (simplified calculation)
    const expectedHits = (stats.hits_per_9 * inningsFactor) / 9; // Per batter
    const expectedWalks = (stats.bb_per_9 * inningsFactor) / 9;
    const expectedStrikeouts = (stats.k_per_9 * inningsFactor) / 9;
    const expectedHomeRuns = (stats.hr_per_9 * inningsFactor) / 9;
    const expectedRuns = (stats.era * inningsFactor) / 9;
    
    // Break down hits into singles, doubles, triples
    // Typical distribution: ~75% singles, ~20% doubles, ~3% triples, ~2% HR
    const expectedSingles = expectedHits * 0.75;
    const expectedDoubles = expectedHits * 0.20;
    const expectedTriples = expectedHits * 0.03;
    
    // Calculate fantasy points
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
    
    return {
      team_abbreviation: teamStats.abbreviation,
      handedness,
      inning,
      expected_fantasy_points: Math.round(totalBattingPoints * 100) / 100,
      expected_runs: Math.round(expectedRuns * 1000) / 1000,
      expected_hits: Math.round(expectedHits * 1000) / 1000,
      expected_singles: Math.round(expectedSingles * 1000) / 1000,
      expected_doubles: Math.round(expectedDoubles * 1000) / 1000,
      expected_triples: Math.round(expectedTriples * 1000) / 1000,
      expected_home_runs: Math.round(expectedHomeRuns * 1000) / 1000,
      expected_walks: Math.round(expectedWalks * 1000) / 1000,
      expected_strikeouts: Math.round(expectedStrikeouts * 1000) / 1000,
      expected_rbi: Math.round(expectedRbi * 1000) / 1000,
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
