import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FantasyExpectedStart.css';

interface FantasyExpectedStartProps {}

interface ScoringSettings {
  hits: number;
  runs: number;
  rbi: number;
  homeRuns: number;
  stolenBases: number;
  walks: number;
  strikeouts: number;
}

interface LeagueSettings {
  type: string;
  scoringSettings: ScoringSettings;
}

interface Player {
  id: number;
  player_name: string;
  team: string;
  position: string;
  handedness: string;
  hits: number;
  runs: number;
  rbi: number;
  home_runs: number;
  stolen_bases: number;
  walks: number;
  strikeouts: number;
  games_played: number;
  at_bats: number;
}

interface ExpectedGameResult {
  player: string;
  expected_hits: string;
  expected_runs: string;
  expected_rbi: string;
  expected_home_runs: string;
  expected_stolen_bases: string;
  expected_walks: string;
  expected_strikeouts: string;
  expected_fantasy_points: string;
}

const FantasyExpectedStart: React.FC<FantasyExpectedStartProps> = () => {
  const [handedness, setHandedness] = useState<string>('Righty');
  const [leagueType, setLeagueType] = useState<string>('Custom');
  const [selectedPlayer, setSelectedPlayer] = useState<string>('');
  const [players, setPlayers] = useState<Player[]>([]);
  const [expectedResult, setExpectedResult] = useState<ExpectedGameResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [scoringSettings, setScoringSettings] = useState<ScoringSettings>({
    hits: 1,
    runs: 1,
    rbi: 1,
    homeRuns: 4,
    stolenBases: 2,
    walks: 1,
    strikeouts: -1
  });

  // ESPN default scoring settings
  const espnSettings: ScoringSettings = {
    hits: 1,
    runs: 1,
    rbi: 1,
    homeRuns: 4,
    stolenBases: 2,
    walks: 1,
    strikeouts: -1
  };

  // CBS default scoring settings
  const cbsSettings: ScoringSettings = {
    hits: 1,
    runs: 1,
    rbi: 1,
    homeRuns: 4,
    stolenBases: 2,
    walks: 1,
    strikeouts: -0.5
  };

  // Yahoo default scoring settings
  const yahooSettings: ScoringSettings = {
    hits: 1,
    runs: 1,
    rbi: 1,
    homeRuns: 4,
    stolenBases: 2,
    walks: 1,
    strikeouts: 0
  };

  // Load players on component mount
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/players');
        setPlayers(response.data);
      } catch (error) {
        console.error('Error fetching players:', error);
      }
    };

    fetchPlayers();
  }, []);

  useEffect(() => {
    // Update scoring settings based on league type
    switch (leagueType) {
      case 'ESPN':
        setScoringSettings(espnSettings);
        break;
      case 'CBS':
        setScoringSettings(cbsSettings);
        break;
      case 'Yahoo':
        setScoringSettings(yahooSettings);
        break;
      default:
        // Keep current custom settings
        break;
    }
  }, [leagueType]);

  const handleScoringChange = (stat: keyof ScoringSettings, value: number) => {
    setScoringSettings(prev => ({
      ...prev,
      [stat]: value
    }));
  };

  const calculateExpectedPoints = async () => {
    if (!selectedPlayer) {
      alert('Please select a player first');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/calculate-expected', {
        player_name: selectedPlayer,
        handedness,
        league_type: leagueType,
        scoring_settings: scoringSettings
      });

      setExpectedResult(response.data);
    } catch (error) {
      console.error('Error calculating expected points:', error);
      alert('Error calculating expected points. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fantasy-expected-start">
      <h1>Fantasy Expected Start</h1>
      
      <div className="form-container">
        <div className="form-group">
          <label htmlFor="handedness">Handedness:</label>
          <select 
            id="handedness"
            value={handedness} 
            onChange={(e) => setHandedness(e.target.value)}
            className="dropdown"
          >
            <option value="Righty">Righty</option>
            <option value="Lefty">Lefty</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="leagueType">League Type:</label>
          <select 
            id="leagueType"
            value={leagueType} 
            onChange={(e) => setLeagueType(e.target.value)}
            className="dropdown"
          >
            <option value="Custom">Custom</option>
            <option value="CBS">CBS</option>
            <option value="ESPN">ESPN</option>
            <option value="Yahoo">Yahoo</option>
          </select>
        </div>

        {leagueType === 'Custom' && (
          <div className="scoring-settings">
            <h3>Custom Scoring Settings</h3>
            <div className="scoring-grid">
              <div className="scoring-item">
                <label>Hits:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.hits}
                  onChange={(e) => handleScoringChange('hits', parseFloat(e.target.value))}
                />
              </div>
              <div className="scoring-item">
                <label>Runs:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.runs}
                  onChange={(e) => handleScoringChange('runs', parseFloat(e.target.value))}
                />
              </div>
              <div className="scoring-item">
                <label>RBI:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.rbi}
                  onChange={(e) => handleScoringChange('rbi', parseFloat(e.target.value))}
                />
              </div>
              <div className="scoring-item">
                <label>Home Runs:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.homeRuns}
                  onChange={(e) => handleScoringChange('homeRuns', parseFloat(e.target.value))}
                />
              </div>
              <div className="scoring-item">
                <label>Stolen Bases:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.stolenBases}
                  onChange={(e) => handleScoringChange('stolenBases', parseFloat(e.target.value))}
                />
              </div>
              <div className="scoring-item">
                <label>Walks:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.walks}
                  onChange={(e) => handleScoringChange('walks', parseFloat(e.target.value))}
                />
              </div>
              <div className="scoring-item">
                <label>Strikeouts:</label>
                <input 
                  type="number" 
                  step="0.1"
                  value={scoringSettings.strikeouts}
                  onChange={(e) => handleScoringChange('strikeouts', parseFloat(e.target.value))}
                />
              </div>
            </div>
          </div>
        )}

        {leagueType !== 'Custom' && (
          <div className="preset-settings">
            <h3>{leagueType} Scoring Settings</h3>
            <div className="settings-display">
              <p>Hits: {scoringSettings.hits}</p>
              <p>Runs: {scoringSettings.runs}</p>
              <p>RBI: {scoringSettings.rbi}</p>
              <p>Home Runs: {scoringSettings.homeRuns}</p>
              <p>Stolen Bases: {scoringSettings.stolenBases}</p>
              <p>Walks: {scoringSettings.walks}</p>
              <p>Strikeouts: {scoringSettings.strikeouts}</p>
            </div>
          </div>
        )}

        <button 
          className="calculate-btn"
          onClick={calculateExpectedPoints}
        >
          Calculate Expected Points
        </button>
      </div>
    </div>
  );
};

export default FantasyExpectedStart;
