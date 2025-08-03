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
    category: 'batting' | 'pitching',
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
   * Render input field for a stat
   */
  const renderStatInput = (
    category: 'batting' | 'pitching',
    stat: string,
    label: string,
    value: number
  ) => (
    <div className=\"stat-input-group\" key={`${category}-${stat}`}>
      <label htmlFor={`${category}-${stat}`} className=\"stat-label\">
        {label}:
      </label>
      <input
        id={`${category}-${stat}`}
        type=\"number\"
        step=\"0.1\"
        value={value}
        onChange={(e) => handleInputChange(category, stat, e.target.value)}
        className=\"stat-input\"
        readOnly={readOnly}
        disabled={readOnly}
      />
    </div>
  );

  return (
    <div className=\"scoring-settings-form\">
      <div className=\"settings-header\">
        <h3>
          {leagueType === 'Custom' ? 'Custom' : leagueType} Scoring Settings
        </h3>
        {readOnly && (
          <p className=\"readonly-notice\">
            These are preset values for {leagueType} leagues and cannot be modified.
          </p>
        )}
      </div>

      <div className=\"settings-grid\">
        {/* Batting Settings */}
        <div className=\"settings-section\">
          <h4 className=\"section-title\">Batting</h4>
          <div className=\"stats-grid\">
            {renderStatInput('batting', 'S', 'Singles', scoringSettings.batting.S)}
            {renderStatInput('batting', 'D', 'Doubles', scoringSettings.batting.D)}
            {renderStatInput('batting', 'T', 'Triples', scoringSettings.batting.T)}
            {renderStatInput('batting', 'HR', 'Home Runs', scoringSettings.batting.HR)}
            {renderStatInput('batting', 'BB', 'Walks', scoringSettings.batting.BB)}
            {renderStatInput('batting', 'IBB', 'Intentional Walks', scoringSettings.batting.IBB)}
            {renderStatInput('batting', 'HBP', 'Hit By Pitch', scoringSettings.batting.HBP)}
            {renderStatInput('batting', 'R', 'Runs', scoringSettings.batting.R)}
            {renderStatInput('batting', 'RBI', 'Runs Batted In', scoringSettings.batting.RBI)}
            {renderStatInput('batting', 'SB', 'Stolen Base', scoringSettings.batting.SB)}
            {renderStatInput('batting', 'CS', 'Caught Stealing', scoringSettings.batting.CS)}
            {renderStatInput('batting', 'SO', 'Strike Outs', scoringSettings.batting.SO)}
            {renderStatInput('batting', 'GIDP', 'Grounded into Double Play', scoringSettings.batting.GIDP)}
            {renderStatInput('batting', 'E', 'Errors', scoringSettings.batting.E)}
          </div>
        </div>

        {/* Pitching Settings */}
        <div className=\"settings-section\">
          <h4 className=\"section-title\">Pitching</h4>
          <div className=\"stats-grid\">
            {renderStatInput('pitching', 'BB', 'Walks Issued', scoringSettings.pitching.BB)}
            {renderStatInput('pitching', 'IBB', 'Intentional Base on Balls', scoringSettings.pitching.IBB)}
            {renderStatInput('pitching', 'ER', 'Earned Runs', scoringSettings.pitching.ER)}
            {renderStatInput('pitching', 'HA', 'Hits Allowed', scoringSettings.pitching.HA)}
            {renderStatInput('pitching', 'HB', 'Hit Batters', scoringSettings.pitching.HB)}
            {renderStatInput('pitching', 'HRA', 'Home Runs Allowed', scoringSettings.pitching.HRA)}
            {renderStatInput('pitching', 'INN', 'Innings (3 outs)', scoringSettings.pitching.INN)}
            {renderStatInput('pitching', 'K', 'Strikeouts', scoringSettings.pitching.K)}
            {renderStatInput('pitching', 'W', 'Wins', scoringSettings.pitching.W)}
            {renderStatInput('pitching', 'L', 'Losses', scoringSettings.pitching.L)}
            {renderStatInput('pitching', 'S', 'Saves', scoringSettings.pitching.S)}
            {renderStatInput('pitching', 'BS', 'Blown Saves', scoringSettings.pitching.BS)}
            {renderStatInput('pitching', 'QS', 'Quality Starts', scoringSettings.pitching.QS)}
            {renderStatInput('pitching', 'TB', 'Total Bases', scoringSettings.pitching.TB)}
            {renderStatInput('pitching', 'Hold', 'Holds', scoringSettings.pitching.Hold)}
            {renderStatInput('pitching', 'WP', 'Wild Pitch', scoringSettings.pitching.WP)}
            {renderStatInput('pitching', 'BK', 'Balk', scoringSettings.pitching.BK)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScoringSettingsForm;

