/**
 * Fantasy Expected Start component - Main component for calculating expected fantasy points
 */
import React, { useState, useEffect, useCallback } from 'react';
import { FantasyBaseballAPI } from '../services/api';
import { LocalStorageManager } from '../utils/localStorage';
import { ColorUtils } from '../utils/colorUtils';
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
  const [showScoringSettings, setShowScoringSettings] = useState<boolean>(false);

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
   * Load scoring settings based on league type
   */
  const loadScoringSettings = useCallback(async () => {
    if (leagueType === 'Custom') {
      // Load default custom settings
      const response = await FantasyBaseballAPI.getScoringSettings('Custom');
      if (response.data) {
        setScoringSettings(response.data.scoring_settings);
      }
      setShowScoringSettings(true);
    } else {
      // Load preset settings
      const response = await FantasyBaseballAPI.getScoringSettings(leagueType);
      if (response.data) {
        setScoringSettings(response.data.scoring_settings);
      }
      setShowScoringSettings(false);
    }
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
   * Calculate expected points for all teams
   */
  const calculateExpectedPoints = async () => {
    if (!scoringSettings) {
      setError('Scoring settings not loaded');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const request = {
        handedness,
        inning,
        league_type: leagueType,
        ...(leagueType === 'Custom' && { custom_scoring: scoringSettings }),
      };

      const response = await FantasyBaseballAPI.calculateExpected(request);
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setResults(response.data);
      }
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

          {/* Scoring Settings Form */}
          {showScoringSettings && scoringSettings && (
            <ScoringSettingsForm
              scoringSettings={scoringSettings}
              onSettingsChange={setScoringSettings}
              readOnly={leagueType !== 'Custom'}
              leagueType={leagueType}
            />
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
          <div className="results-section">
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

