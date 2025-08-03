/**
 * Fantasy Expected Start component - Main component for calculating expected fantasy points
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { FantasyBaseballAPI } from '../services/api';
import { LocalStorageManager } from '../utils/localStorage';
import { ColorUtils } from '../utils/colorUtils';
import { FantasyCalculations, TeamStats } from '../utils/fantasyCalculations';
import {
  ScoringSettings,
  LeagueType,
  Handedness,
  MatchupAnalysisResult,
  ExpectedGameResult,
  CustomLeague
} from '../types';
import ScoringSettingsForm from './ScoringSettingsForm';
import TeamMatchupGrid from './TeamMatchupGrid';
import Accordion from './Accordion';
import './FantasyExpectedStart.css';

const FantasyExpectedStart: React.FC = () => {
  // Form state
  const [handedness, setHandedness] = useState<Handedness>('Righty');
  const [leagueType, setLeagueType] = useState<LeagueType>('Custom');
  const [inning, setInning] = useState<number>(6);
  const [leagueName, setLeagueName] = useState<string>('');
  
  // Scoring settings state
  const [scoringSettings, setScoringSettings] = useState<ScoringSettings | null>(null);
  const [customLeagues, setCustomLeagues] = useState<string[]>([]);
  
  // Results state
  const [results, setResults] = useState<MatchupAnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // UI state
  const [showScoringSettings, setShowScoringSettings] = useState<boolean>(true);
  
  // Refs for scrolling
  const resultsRef = useRef<HTMLDivElement>(null);

  /**
   * Load custom leagues from localStorage on component mount
   */
  useEffect(() => {
    const leagues = LocalStorageManager.getCustomLeagueNames();
    setCustomLeagues(leagues);
  }, []);

  /**
   * Load scoring settings when league type changes
   */
  useEffect(() => {
    loadScoringSettings();
  }, [leagueType]);

  /**
   * Get hardcoded scoring settings based on league type
   */
  const getHardcodedScoringSettings = (league: LeagueType): ScoringSettings => {
    switch (league) {
      case 'Custom':
        return {
          batting: {
            S: 1.0,    // Singles
            D: 2.0,    // Doubles
            T: 3.0,    // Triples
            HR: 4.0,   // Home Runs
            BB: 1.0,   // Walks
            IBB: 1.0,  // Intentional Walks
            HBP: 1.0,  // Hit By Pitch
            R: 1.0,    // Runs
            RBI: 1.0,  // Runs Batted In
            SB: 1.0,   // Stolen Base
            CS: -1.0,  // Caught Stealing
            SO: 0.5,   // Strike Outs
            GIDP: 0.0, // Grounded into Double Play
            E: 0.0     // Errors
          },
          pitching: {
            BB: -1.0,   // Walks Issued
            IBB: -1.0,  // Intentional Base on Balls
            ER: -1.0,   // Earned Runs
            HA: -1.0,   // Hits allowed
            HB: -1.0,   // Hit Batters
            HRA: -1.0,  // Home Runs Allowed
            INN: 3.0,   // Innings
            K: 0.5,     // Strikeouts
            W: 2.0,     // Wins
            L: -1.0,    // Losses
            S: 2.0,     // Saves
            BS: -1.0,   // Blown Saves
            QS: 2.0,    // Quality Starts
            TB: 0.0,    // Total Bases
            Hold: 0.0,  // Holds
            WP: 0.0,    // Wild Pitch
            BK: 0.0     // Balk
          }
        };
      case 'ESPN':
        return {
          batting: {
            S: 1.0,
            D: 2.0,
            T: 3.0,
            HR: 4.0,
            BB: 1.0,
            IBB: 0.0,
            HBP: 0.0,
            R: 1.0,
            RBI: 1.0,
            SB: 1.0,
            CS: 0.0,
            SO: -1.0,
            GIDP: 0.0,
            E: 0.0
          },
          pitching: {
            BB: -1.0,
            IBB: -1.0,
            ER: -1.0,
            HA: -1.0,
            HB: 0.0,
            HRA: -1.0,
            INN: 3.0,
            K: 1.0,
            W: 2.0,
            L: -1.0,
            S: 2.0,
            BS: 0.0,
            QS: 0.0,
            TB: 0.0,
            Hold: 0.0,
            WP: 0.0,
            BK: 0.0
          }
        };
      case 'CBS':
        return {
          batting: {
            S: 1.0,
            D: 2.0,
            T: 3.0,
            HR: 4.0,
            BB: 1.0,
            IBB: 1.0,
            HBP: 1.0,
            R: 1.0,
            RBI: 1.0,
            SB: 2.0,
            CS: -1.0,
            SO: -1.0,
            GIDP: 0.0,
            E: 0.0
          },
          pitching: {
            BB: -1.0,
            IBB: -1.0,
            ER: -1.0,
            HA: -1.0,
            HB: 0.0,
            HRA: -1.0,
            INN: 3.0,
            K: 1.0,
            W: 5.0,
            L: -3.0,
            S: 2.0,
            BS: -2.0,
            QS: 0.0,
            TB: 0.0,
            Hold: 0.0,
            WP: 0.0,
            BK: 0.0
          }
        };
      case 'Yahoo':
        return {
          batting: {
            S: 1.0,
            D: 2.0,
            T: 3.0,
            HR: 4.0,
            BB: 1.0,
            IBB: 1.0,
            HBP: 1.0,
            R: 1.0,
            RBI: 1.0,
            SB: 2.0,
            CS: -1.0,
            SO: -1.0,
            GIDP: 0.0,
            E: 0.0
          },
          pitching: {
            BB: -1.0,
            IBB: -1.0,
            ER: -1.0,
            HA: -1.0,
            HB: 0.0,
            HRA: -1.0,
            INN: 3.0,
            K: 1.0,
            W: 5.0,
            L: -3.0,
            S: 2.0,
            BS: -2.0,
            QS: 0.0,
            TB: 0.0,
            Hold: 0.0,
            WP: 0.0,
            BK: 0.0
          }
        };
      default:
        return getHardcodedScoringSettings('Custom');
    }
  };

  /**
   * Load scoring settings based on league type (now using hardcoded values)
   */
  const loadScoringSettings = useCallback(() => {
    const settings = getHardcodedScoringSettings(leagueType);
    setScoringSettings(settings);
    
    // Always show scoring settings for all league types
    setShowScoringSettings(true);
  }, [leagueType]);

  /**
   * Handle league type change
   */
  const handleLeagueTypeChange = (newLeagueType: string) => {
    if (customLeagues.includes(newLeagueType)) {
      // Load custom league
      const customLeague = LocalStorageManager.getCustomLeague(newLeagueType);
      if (customLeague) {
        setLeagueType('Custom');
        setScoringSettings(customLeague.scoring_settings);
        setLeagueName(newLeagueType);
        setShowScoringSettings(true);
      }
    } else {
      // Standard league type
      setLeagueType(newLeagueType as LeagueType);
      setLeagueName('');
    }
  };

  /**
   * Save custom league to localStorage
   */
  const saveCustomLeague = () => {
    if (!leagueName.trim()) {
      setError('Please enter a league name');
      return;
    }

    if (!scoringSettings) {
      setError('Scoring settings not loaded');
      return;
    }

    const customLeague: CustomLeague = {
      name: leagueName.trim(),
      scoring_settings: scoringSettings,
      created_at: new Date().toISOString(),
    };

    LocalStorageManager.saveCustomLeague(customLeague);
    
    // Update custom leagues list
    const updatedLeagues = LocalStorageManager.getCustomLeagueNames();
    setCustomLeagues(updatedLeagues);
    
    setError(null);
    alert(`Custom league "${leagueName}" saved successfully!`);
  };

  /**
   * Calculate expected points for all teams using frontend calculations
   */
  const calculateExpectedPoints = async () => {
    if (!scoringSettings) {
      setError('Scoring settings not loaded');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Fetch team stats from backend
      const response = await FantasyBaseballAPI.getTeamStats();
      
      if (response.error) {
        setError(response.error);
        return;
      }

      if (!response.data || !response.data.teams) {
        setError('No team data received');
        return;
      }

      // Calculate expected points using frontend logic
      const teamStats: TeamStats[] = response.data.teams;
      const calculationResults = FantasyCalculations.calculateAllTeamsExpectedPoints(
        teamStats,
        handedness,
        inning,
        scoringSettings
      );

      // Add color coding for visualization
      const resultsWithColors = FantasyCalculations.addColorCoding(calculationResults);

      // Calculate analysis summary
      const points = calculationResults.map(r => r.expected_fantasy_points);
      const minPoints = Math.min(...points);
      const maxPoints = Math.max(...points);
      const avgPoints = points.reduce((sum, p) => sum + p, 0) / points.length;

      // Format results to match expected structure
      const formattedResults: MatchupAnalysisResult = {
        results: resultsWithColors,
        parameters: {
          handedness,
          inning,
          league_type: leagueType
        },
        analysis: {
          min_points: minPoints,
          max_points: maxPoints,
          avg_points: avgPoints,
          total_teams: calculationResults.length
        }
      };

      setResults(formattedResults);
      
      // Collapse scoring settings accordion and scroll to results
      setShowScoringSettings(false);
      setTimeout(() => {
        if (resultsRef.current) {
          resultsRef.current.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
          });
        }
      }, 300); // Wait for accordion collapse animation
      
    } catch (err) {
      setError('Failed to calculate expected points');
      console.error('Calculation error:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle inning input change with validation
   */
  const handleInningChange = (value: string) => {
    const numValue = parseInt(value, 10);
    if (!isNaN(numValue) && numValue >= 1 && numValue <= 9) {
      setInning(numValue);
    }
  };

  /**
   * Get all available league options for dropdown
   */
  const getLeagueOptions = () => {
    const standardOptions = ['Custom', 'ESPN', 'CBS', 'Yahoo'];
    return [...standardOptions, ...customLeagues];
  };

  return (
    <div className="fantasy-expected-start">
      <div className="container">
        <header className="header">
          <h1>Fantasy Expected Start</h1>
          <p className="subtitle">
            Calculate expected fantasy points for MLB team matchups
          </p>
        </header>

        <div className="form-section">
          <div className="form-grid">
            {/* Handedness Dropdown */}
            <div className="form-group">
              <label htmlFor="handedness">Batter Handedness:</label>
              <select
                id="handedness"
                value={handedness}
                onChange={(e) => setHandedness(e.target.value as Handedness)}
                className="form-control"
              >
                <option value="Righty">Righty</option>
                <option value="Lefty">Lefty</option>
              </select>
            </div>

            {/* League Type Dropdown */}
            <div className="form-group">
              <label htmlFor="leagueType">League Type:</label>
              <select
                id="leagueType"
                value={leagueType === 'Custom' && leagueName ? leagueName : leagueType}
                onChange={(e) => handleLeagueTypeChange(e.target.value)}
                className="form-control"
              >
                {getLeagueOptions().map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>

            {/* Inning Input */}
            <div className="form-group">
              <label htmlFor="inning">Innings:</label>
              <input
                id="inning"
                type="number"
                min="1"
                max="9"
                value={inning}
                onChange={(e) => handleInningChange(e.target.value)}
                className="form-control"
              />
              <small className="form-text">Enter innings (1-9)</small>
            </div>

            {/* League Name Input (for custom leagues) */}
            {leagueType === 'Custom' && (
              <div className="form-group">
                <label htmlFor="leagueName">League Name (optional):</label>
                <div className="input-group">
                  <input
                    id="leagueName"
                    type="text"
                    value={leagueName}
                    onChange={(e) => setLeagueName(e.target.value)}
                    placeholder="Enter name to save custom league"
                    className="form-control"
                  />
                  <button
                    type="button"
                    onClick={saveCustomLeague}
                    className="btn btn-secondary"
                    disabled={!leagueName.trim() || !scoringSettings}
                  >
                    Save
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Scoring Settings Accordion */}
          {scoringSettings && (
            <Accordion
              title="Scoring Settings"
              isOpen={showScoringSettings}
              onToggle={() => setShowScoringSettings(!showScoringSettings)}
              className="scoring-settings-accordion"
            >
              <ScoringSettingsForm
                scoringSettings={scoringSettings}
                onSettingsChange={setScoringSettings}
                readOnly={leagueType !== 'Custom'}
                leagueType={leagueType}
              />
            </Accordion>
          )}

          {/* Error Display */}
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}

          {/* Calculate Button */}
          <div className="calculate-section">
            <button
              onClick={calculateExpectedPoints}
              disabled={loading || !scoringSettings}
              className="btn btn-primary btn-lg"
            >
              {loading ? 'Calculating...' : 'Calculate Expected Points'}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results && (
          <div className="results-section" ref={resultsRef}>
            <div className="results-header">
              <h2>Team Matchup Analysis</h2>
              <div className="results-summary">
                <p>
                  <strong>Parameters:</strong> {results.parameters.handedness} batter, 
                  {results.parameters.inning} innings, {results.parameters.league_type} scoring
                </p>
                <p>
                  <strong>Range:</strong> {results.analysis.min_points.toFixed(2)} - 
                  {results.analysis.max_points.toFixed(2)} points 
                  (Avg: {results.analysis.avg_points.toFixed(2)})
                </p>
              </div>
            </div>

            <TeamMatchupGrid results={results.results} />
          </div>
        )}
      </div>
    </div>
  );
};

export default FantasyExpectedStart;
