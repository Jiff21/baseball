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
    // Development logging
    const isDevelopment = process.env.NODE_ENV === 'development';
    
    if (isDevelopment) {
      console.log(`\n🏟️ FRONTEND CALCULATION: ${teamStats.name} (${teamStats.abbreviation})`);
      console.log(`📊 Handedness: ${handedness} | Expected Innings: ${expectedInnings}`);
      console.log('='.repeat(60));
    }
    
    // Select appropriate stats based on handedness
    const stats = handedness.toLowerCase() === 'lefty' ? teamStats.vs_lefty : teamStats.vs_righty;
    
    if (isDevelopment) {
      console.log(`📈 RAW TEAM STATS vs ${handedness.toUpperCase()}:`);
      console.log(`   ERA: ${stats.era} | Runs allowed per 9 innings`);
      console.log(`   WHIP: ${stats.whip} | Walks + Hits per inning`);
      console.log(`   K/9: ${stats.k_per_9} | Strikeouts per 9 innings`);
      console.log(`   BB/9: ${stats.bb_per_9} | Walks per 9 innings`);
      console.log(`   HR/9: ${stats.hr_per_9} | Home runs per 9 innings`);
      console.log(`   Hits/9: ${stats.hits_per_9} | Hits allowed per 9 innings`);
    }
    
    // Calculate PA per inning multiplier if data is available
    let paPerInning = 1.0; // Default multiplier
    if (teamStats.total_plate_appearances && teamStats.games_played) {
      // Formula: (Total plate appearances / games played) / 9
      paPerInning = (teamStats.total_plate_appearances / teamStats.games_played) / 9;
    }
    
    // Calculate expected stats per inning using expectedInnings (from form)
    const inningsFactor = expectedInnings / 9.0;
    
    if (isDevelopment) {
      console.log(`\n🧮 PER_9 CALCULATIONS:`);
      console.log(`   Innings Factor: ${expectedInnings}/9 = ${inningsFactor.toFixed(4)}`);
      console.log(`   PA per Inning: ${paPerInning.toFixed(2)} (${teamStats.total_plate_appearances ? 'calculated' : 'default'})`);
    }
    
    // Basic expected stats (simplified calculation) - all multiplied by expectedInnings
    const expectedHits = (stats.hits_per_9 * inningsFactor);
    const expectedWalks = (stats.bb_per_9 * inningsFactor);
    const expectedStrikeouts = (stats.k_per_9 * inningsFactor);
    const expectedHomeRuns = (stats.hr_per_9 * inningsFactor);
    const expectedRuns = (stats.era * inningsFactor);
    
    if (isDevelopment) {
      console.log(`   Expected Hits: (${stats.hits_per_9} * ${inningsFactor.toFixed(4)}) = ${expectedHits.toFixed(6)}`);
      console.log(`   Expected Walks: (${stats.bb_per_9} * ${inningsFactor.toFixed(4)}) = ${expectedWalks.toFixed(6)}`);
      console.log(`   Expected Strikeouts: (${stats.k_per_9} * ${inningsFactor.toFixed(4)}) = ${expectedStrikeouts.toFixed(6)}`);
      console.log(`   Expected Home Runs: (${stats.hr_per_9} * ${inningsFactor.toFixed(4)}) = ${expectedHomeRuns.toFixed(6)}`);
      console.log(`   Expected Runs: (${stats.era} * ${inningsFactor.toFixed(4)}) = ${expectedRuns.toFixed(6)}`);
    }
    
    // Calculate wins and losses per game if data is available
    let winsPerGame = 0;
    let lossesPerGame = 0;
    
    // Get wins/losses from the correct nested structure based on handedness
    const teamWins = handedness.toLowerCase() === 'lefty' ? teamStats.vs_lefty.wins : teamStats.vs_righty.wins;
    const teamLosses = handedness.toLowerCase() === 'lefty' ? teamStats.vs_lefty.losses : teamStats.vs_righty.losses;
    
    if (teamWins !== undefined && teamLosses !== undefined) {
      const totalGames = teamWins + teamLosses;
      if (totalGames > 0) {
        winsPerGame = teamWins / totalGames;
        lossesPerGame = teamLosses / totalGames;
      }
    }
    
    if (isDevelopment) {
      console.log(`\n🏆 WINS/LOSSES CALCULATION:`);
      console.log(`   Team Wins vs ${handedness}: ${teamWins}`);
      console.log(`   Team Losses vs ${handedness}: ${teamLosses}`);
      console.log(`   Total Games: ${teamWins + teamLosses}`);
      console.log(`   Wins Per Game: ${winsPerGame.toFixed(6)}`);
      console.log(`   Losses Per Game: ${lossesPerGame.toFixed(6)}`);
    }
    
    // Break down hits into singles, doubles, triples for display purposes only
    // Typical distribution: ~75% singles, ~20% doubles, ~3% triples, ~2% HR
    const expectedSingles = expectedHits * 0.75;
    const expectedDoubles = expectedHits * 0.20;
    const expectedTriples = expectedHits * 0.03;
    
    if (isDevelopment) {
      console.log(`\n⚾ HIT BREAKDOWN (Distribution):`);
      console.log(`   Expected Singles: ${expectedHits.toFixed(6)} * 0.75 = ${expectedSingles.toFixed(6)}`);
      console.log(`   Expected Doubles: ${expectedHits.toFixed(6)} * 0.20 = ${expectedDoubles.toFixed(6)}`);
      console.log(`   Expected Triples: ${expectedHits.toFixed(6)} * 0.03 = ${expectedTriples.toFixed(6)}`);
      console.log(`   Expected Home Runs: ${expectedHomeRuns.toFixed(6)} (from HR/9 stat)`);
    }
    
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
    
    if (isDevelopment) {
      console.log(`\n💰 FANTASY POINTS CALCULATION:`);
      console.log(`   Pitching Scoring Settings:`, scoringSettings.pitching);
      console.log(`   Innings Points: ${expectedInnings} * ${scoringSettings.pitching.INN} = ${pitchingInningsPoints.toFixed(6)}`);
      console.log(`   Walks: ${expectedWalks.toFixed(6)} * ${scoringSettings.pitching.BB} = ${(expectedWalks * scoringSettings.pitching.BB).toFixed(6)}`);
      console.log(`   Earned Runs: ${expectedRuns.toFixed(6)} * ${scoringSettings.pitching.ER} = ${(expectedRuns * scoringSettings.pitching.ER).toFixed(6)}`);
      console.log(`   Hits Allowed: ${expectedHits.toFixed(6)} * ${scoringSettings.pitching.HA} = ${(expectedHits * scoringSettings.pitching.HA).toFixed(6)}`);
      console.log(`   HR Allowed: ${expectedHomeRuns.toFixed(6)} * ${scoringSettings.pitching.HRA} = ${(expectedHomeRuns * scoringSettings.pitching.HRA).toFixed(6)}`);
      console.log(`   Strikeouts: ${expectedStrikeouts.toFixed(6)} * ${scoringSettings.pitching.K} = ${(expectedStrikeouts * scoringSettings.pitching.K).toFixed(6)}`);
      console.log(`   Wins: ${(winsPerGame * expectedInnings / 9).toFixed(6)} * ${scoringSettings.pitching.W} = ${((winsPerGame * expectedInnings / 9) * scoringSettings.pitching.W).toFixed(6)}`);
      console.log(`   Losses: ${(lossesPerGame * expectedInnings / 9).toFixed(6)} * ${scoringSettings.pitching.L} = ${((lossesPerGame * expectedInnings / 9) * scoringSettings.pitching.L).toFixed(6)}`);
      console.log(`   TOTAL PITCHING POINTS: ${pitchingPoints.toFixed(6)}`);
    }
    
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
      
      if (deviationsFromMean >= 1.5) {
        // 1.5 standard deviations above average = Good (Green)
        colorCategory = 'good';
        colorScore = 1.0;
      } else if (deviationsFromMean <= -1.5) {
        // 1.5 standard deviations below average = Bad (Red)
        colorCategory = 'bad';
        colorScore = 0.0;
      } else {
        // Within 1.5 standard deviations = Average (No color)
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
