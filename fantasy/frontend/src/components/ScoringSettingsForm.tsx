/**
 * Scoring Settings Form component for customizing fantasy scoring
 */
import React from 'react';
import { ScoringSettings, LeagueType } from '../types';

interface ScoringSettingsFormProps {
  scoringSettings: ScoringSettings;
  onSettingsChange: (settings: ScoringSettings) => void;
  readOnly: boolean;
  leagueType: LeagueType;
}

const ScoringSettingsForm: React.FC<ScoringSettingsFormProps> = ({
  scoringSettings,
  onSettingsChange,
  readOnly,
  leagueType
}) => {
  /**
   * Handle input change for scoring settings
   */
  const handleInputChange = (
    category: 'pitching',
    stat: string,
    value: string
  ) => {
    if (readOnly) return;

    const numValue = parseFloat(value) || 0;
    const updatedSettings = {
      ...scoringSettings,
      [category]: {
        ...scoringSettings[category],
        [stat]: numValue
      }
    };
    
    onSettingsChange(updatedSettings);
  };

  /**
   * Render input field for a stat with inline layout
   */
  const renderStatInput = (
    category: 'pitching',
    stat: string,
    label: string,
    value: number
  ) => {
    // Special handling for innings - use dropdown
    const isInnings = stat === 'INN';
    
    if (isInnings) {
      const inningsOptions = [
        3.0, 3.3, 3.6, 4.0, 4.3, 4.6, 5.0, 5.3, 5.6, 
        6.0, 6.3, 6.6, 7.0, 7.3, 7.6, 8.0, 8.3, 8.6, 9.0
      ];
      
      return (
        <div className="stat-input-inline" key={`${category}-${stat}`}>
          <label htmlFor={`${category}-${stat}`} className="stat-label-inline">
            {label}:
          </label>
          <select
            id={`${category}-${stat}`}
            value={value.toFixed(1)}
            onChange={(e) => handleInputChange(category, stat, e.target.value)}
            className="stat-select-inline"
            disabled={readOnly}
          >
            {inningsOptions.map(option => (
              <option key={option} value={option.toFixed(1)}>
                {option.toFixed(1)}
              </option>
            ))}
          </select>
        </div>
      );
    }
    
    return (
      <div className="stat-input-inline" key={`${category}-${stat}`}>
        <label htmlFor={`${category}-${stat}`} className="stat-label-inline">
          {label}:
        </label>
        <input
          id={`${category}-${stat}`}
          type="number"
          step="0.1"
          max="999"
          min="-999"
          value={value.toFixed(1)}
          onChange={(e) => handleInputChange(category, stat, e.target.value)}
          className="stat-input-inline"
          readOnly={readOnly}
          disabled={readOnly}
        />
      </div>
    );
  };

  return (
    <div className="scoring-settings-form">
      <div className="settings-header">
        <h3>
          Scoring Settings
        </h3>
        {readOnly && (
          <p className="readonly-notice">
            These are preset values for {leagueType} leagues and cannot be modified.
          </p>
        )}
      </div>

      <div className="settings-sections">
        {/* Pitching Settings */}
        <div className="settings-section">
          <h4 className="section-title">Pitching</h4>
          <div className="stats-inline-grid">
            {renderStatInput('pitching', 'BB', 'Walks Issued', scoringSettings.pitching.BB)}
            {renderStatInput('pitching', 'IBB', 'Intentional Base on Balls', scoringSettings.pitching.IBB)}
            {renderStatInput('pitching', 'ER', 'Earned Runs', scoringSettings.pitching.ER)}
            {renderStatInput('pitching', 'HA', 'Hits Allowed', scoringSettings.pitching.HA)}
            {renderStatInput('pitching', 'HB', 'Hit Batters', scoringSettings.pitching.HB)}
            {renderStatInput('pitching', 'HRA', 'Home Runs Allowed', scoringSettings.pitching.HRA)}
            {renderStatInput('pitching', 'INN', 'Innings', scoringSettings.pitching.INN)}
            {renderStatInput('pitching', 'K', 'Strikeouts', scoringSettings.pitching.K)}
            {renderStatInput('pitching', 'W', 'Wins', scoringSettings.pitching.W)}
            {renderStatInput('pitching', 'L', 'Losses', scoringSettings.pitching.L)}
            {renderStatInput('pitching', 'S', 'Saves', scoringSettings.pitching.S)}
            {renderStatInput('pitching', 'BS', 'Blown Saves', scoringSettings.pitching.BS)}
            {renderStatInput('pitching', 'QS', 'Quality Starts', scoringSettings.pitching.QS)}
            {renderStatInput('pitching', 'TB', 'Total Bases', scoringSettings.pitching.TB)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScoringSettingsForm;
