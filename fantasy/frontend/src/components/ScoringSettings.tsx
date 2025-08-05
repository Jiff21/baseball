/**
 * Comprehensive Scoring Settings component for league setup
 * Includes both batting and pitching sections as requested
 */
import React, { useState, useEffect } from 'react';
import './ScoringSettings.css';

interface ScoringSettingsData {
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
    TB: number;     // Total Bases
  };
  pitching: {
    BB: number;     // Walks Issued
    IBB: number;    // Intentional Base on Balls
    ER: number;     // Earned Runs
    HA: number;     // Hits allowed
    HB: number;     // Hit Batters
    HRA: number;    // Home Runs Allowed
    INN: number;    // Innings
    K: number;      // Strikeouts
    W: number;      // Wins
    L: number;      // Losses
    S: number;      // Saves
    BS: number;     // Blown Saves
    QS: number;     // Quality Starts
    TB: number;     // Total Bases
  };
}

interface ScoringSettingsProps {
  onSettingsChange?: (settings: ScoringSettingsData) => void;
  initialSettings?: ScoringSettingsData;
  readOnly?: boolean;
  leagueType?: string;
}

const defaultSettings: ScoringSettingsData = {
  batting: {
    S: 1,      // Singles
    D: 2,      // Doubles
    T: 3,      // Triples
    HR: 4,     // Home Runs
    BB: 1,     // Walks
    IBB: 1,    // Intentional Walks
    HBP: 1,    // Hit By Pitch
    R: 1,      // Runs
    RBI: 1,    // Runs Batted In
    SB: 2,     // Stolen Base
    CS: -1,    // Caught Stealing
    SO: -1,    // Strike Outs
    TB: 0.25,  // Total Bases
  },
  pitching: {
    BB: -1.0,    // Walks Issued
    IBB: -1.0,   // Intentional Base on Balls
    ER: -1.0,    // Earned Runs
    HA: -1.0,    // Hits allowed
    HB: -1.0,    // Hit Batters
    HRA: -3.0,   // Home Runs Allowed
    INN: 3.0,    // Innings
    K: 1.0,      // Strikeouts
    W: 5.0,      // Wins
    L: -3.0,     // Losses
    S: 5.0,      // Saves
    BS: 0.0,     // Blown Saves
    QS: 0.0,     // Quality Starts
    TB: -0.25,   // Total Bases
  }
};

const ScoringSettings: React.FC<ScoringSettingsProps> = ({
  onSettingsChange,
  initialSettings,
  readOnly = false,
  leagueType = 'Custom'
}) => {
  const [settings, setSettings] = useState<ScoringSettingsData>(
    initialSettings || defaultSettings
  );

  useEffect(() => {
    if (initialSettings) {
      setSettings(initialSettings);
    }
  }, [initialSettings]);

  const handleInputChange = (
    category: 'batting' | 'pitching',
    stat: string,
    value: string
  ) => {
    if (readOnly) return;

    const numValue = parseFloat(value) || 0;
    const updatedSettings = {
      ...settings,
      [category]: {
        ...settings[category],
        [stat]: numValue
      }
    };
    
    setSettings(updatedSettings);
    if (onSettingsChange) {
      onSettingsChange(updatedSettings);
    }
  };

  const renderStatInput = (
    category: 'batting' | 'pitching',
    stat: string,
    label: string,
    value: number
  ) => {
    return (
      <div className="scoring-stat-input" key={`${category}-${stat}`}>
        <label htmlFor={`${category}-${stat}`} className="scoring-stat-label">
          {label}
        </label>
        <input
          id={`${category}-${stat}`}
          type="number"
          step="0.1"
          max="999"
          min="-999"
          value={value.toFixed(1)}
          onChange={(e) => handleInputChange(category, stat, e.target.value)}
          className="scoring-stat-value"
          readOnly={readOnly}
          disabled={readOnly}
        />
      </div>
    );
  };

  return (
    <div className="scoring-settings-container">
      <div className="scoring-settings-header">
        <h2>Scoring Settings</h2>
        {readOnly && (
          <p className="readonly-notice">
            These are preset values for {leagueType} leagues and cannot be modified.
          </p>
        )}
      </div>

      <div className="scoring-sections">
        {/* Batting Section */}
        <div className="scoring-section">
          <h3 className="section-title">Batting</h3>
          <div className="scoring-stats-grid">
            {renderStatInput('batting', 'S', 'Singles', settings.batting.S)}
            {renderStatInput('batting', 'D', 'Doubles', settings.batting.D)}
            {renderStatInput('batting', 'T', 'Triples', settings.batting.T)}
            {renderStatInput('batting', 'HR', 'Home Runs', settings.batting.HR)}
            {renderStatInput('batting', 'BB', 'Walks', settings.batting.BB)}
            {renderStatInput('batting', 'IBB', 'Intentional Walks', settings.batting.IBB)}
            {renderStatInput('batting', 'HBP', 'Hit By Pitch', settings.batting.HBP)}
            {renderStatInput('batting', 'R', 'Runs', settings.batting.R)}
            {renderStatInput('batting', 'RBI', 'Runs Batted In', settings.batting.RBI)}
            {renderStatInput('batting', 'SB', 'Stolen Base', settings.batting.SB)}
            {renderStatInput('batting', 'CS', 'Caught Stealing', settings.batting.CS)}
            {renderStatInput('batting', 'SO', 'Strike Outs', settings.batting.SO)}
            {renderStatInput('batting', 'TB', 'Total Bases', settings.batting.TB)}
          </div>
        </div>

        {/* Pitching Section */}
        <div className="scoring-section">
          <h3 className="section-title">Pitching</h3>
          <div className="scoring-stats-grid">
            {renderStatInput('pitching', 'BB', 'Walks Issued', settings.pitching.BB)}
            {renderStatInput('pitching', 'IBB', 'Intentional Base on Balls', settings.pitching.IBB)}
            {renderStatInput('pitching', 'ER', 'Earned Runs', settings.pitching.ER)}
            {renderStatInput('pitching', 'HA', 'Hits allowed', settings.pitching.HA)}
            {renderStatInput('pitching', 'HB', 'Hit Batters', settings.pitching.HB)}
            {renderStatInput('pitching', 'HRA', 'Home Runs Allowed', settings.pitching.HRA)}
            {renderStatInput('pitching', 'INN', 'Innings', settings.pitching.INN)}
            {renderStatInput('pitching', 'K', 'Strikeouts', settings.pitching.K)}
            {renderStatInput('pitching', 'W', 'Wins', settings.pitching.W)}
            {renderStatInput('pitching', 'L', 'Losses', settings.pitching.L)}
            {renderStatInput('pitching', 'S', 'Saves', settings.pitching.S)}
            {renderStatInput('pitching', 'BS', 'Blown Saves', settings.pitching.BS)}
            {renderStatInput('pitching', 'QS', 'Quality Starts', settings.pitching.QS)}
            {renderStatInput('pitching', 'TB', 'Total Bases', settings.pitching.TB)}
          </div>
        </div>
      </div>

      {!readOnly && (
        <div className="scoring-settings-actions">
          <button 
            className="reset-button"
            onClick={() => {
              setSettings(defaultSettings);
              if (onSettingsChange) {
                onSettingsChange(defaultSettings);
              }
            }}
          >
            Reset to Default
          </button>
        </div>
      )}
    </div>
  );
};

export default ScoringSettings;
