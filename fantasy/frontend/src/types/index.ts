/**
 * TypeScript type definitions for the Fantasy Baseball application.
 */

export interface ScoringSettings {
  batting: {
    S: number;      // Singles
    D: number;      // Doubles
    T: number;      // Triples
    HR: number;     // Home Runs
    BB: number;     // Walks
    IBB: number;    // Intentional Walks
    HBP: number;    // Hit By Pitch
    R: number;      // Runs
    RBI: number;    // Runs Batted In
    SB: number;     // Stolen Base
    CS: number;     // Caught Stealing
    SO: number;     // Strike Outs
    GIDP: number;   // Grounded into double play
    E: number;      // Errors
  };
  pitching: {
    BB: number;     // Walks Issued
    IBB: number;    // IBB
    ER: number;     // Earned Runs
    HA: number;     // Hits allowed
    HB: number;     // Hit Batters
    HRA: number;    // HRA
    INN: number;    // Innings (3 outs)
    K: number;      // Strikeouts
    W: number;      // Wins
    L: number;      // Losses
    S: number;      // Saves
    BS: number;     // Blown Saves
    QS: number;     // Quality Starts
    TB: number;     // Total Bases
    Hold: number;   // Holds
    WP: number;     // Wild Pitch
    BK: number;     // Balk
  };
}

export interface Team {
  id: number;
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
  created_at?: string;
  updated_at?: string;
}

export interface FantasyExpectedStartScore {
  team_abbreviation: string;
  handedness: string;
  inning: number;
  expected_fantasy_points: number;
  batting_points: number;
  pitching_points: number;
  pa_per_inning: number; // PA per I - plate appearances per inning
  expected_runs: number;
  expected_hits: number;
  expected_singles: number;
  expected_doubles: number;
  expected_triples: number;
  expected_home_runs: number;
  expected_walks: number;
  expected_strikeouts: number;
  expected_rbi: number;
  expected_wins: number;
  expected_losses: number;
  team_stats: {
    era: number;
    whip: number;
    k_per_9: number;
    bb_per_9: number;
    hr_per_9: number;
    hits_per_9: number;
  };
  color_score?: number;
  color_category?: 'excellent' | 'good' | 'average' | 'poor';
}

export interface MatchupAnalysisResult {
  results: FantasyExpectedStartScore[];
  analysis: {
    min_points: number;
    max_points: number;
    avg_points: number;
    total_teams: number;
  };
  parameters: {
    handedness: string;
    inning: number;
    league_type: string;
  };
}

export interface CustomLeague {
  name: string;
  scoring_settings: ScoringSettings;
  created_at: string;
}

export type LeagueType = 'Custom' | 'ESPN' | 'CBS' | 'Yahoo';
export type Handedness = 'Lefty' | 'Righty';

export interface CalculateExpectedRequest {
  handedness: Handedness;
  inning: number;
  league_type: LeagueType;
  custom_scoring?: ScoringSettings;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}
