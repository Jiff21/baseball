/**
 * Team Matchup Grid component for displaying color-coded team analysis
 */
import React, { useState } from 'react';
import { ExpectedGameResult } from '../types';
import { ColorUtils } from '../utils/colorUtils';

interface TeamMatchupGridProps {
  results: ExpectedGameResult[];
}

const TeamMatchupGrid: React.FC<TeamMatchupGridProps> = ({ results }) => {
  const [sortBy, setSortBy] = useState<'points' | 'team'>('points');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);

  /**
   * Sort results based on current sort settings
   */
  const sortedResults = React.useMemo(() => {
    const sorted = [...results].sort((a, b) => {
      let comparison = 0;
      
      if (sortBy === 'points') {
        comparison = a.expected_fantasy_points - b.expected_fantasy_points;
      } else {
        comparison = a.team_abbreviation.localeCompare(b.team_abbreviation);
      }
      
      return sortOrder === 'asc' ? comparison : -comparison;
    });
    
    return sorted;
  }, [results, sortBy, sortOrder]);

  /**
   * Handle sort change
   */
  const handleSort = (newSortBy: 'points' | 'team') => {
    if (sortBy === newSortBy) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(newSortBy);
      setSortOrder(newSortBy === 'points' ? 'desc' : 'asc');
    }
  };

  /**
   * Handle team selection for detailed view
   */
  const handleTeamClick = (teamAbbr: string) => {
    setSelectedTeam(selectedTeam === teamAbbr ? null : teamAbbr);
  };

  /**
   * Get team details for selected team
   */
  const getSelectedTeamDetails = () => {
    if (!selectedTeam) return null;
    return results.find(r => r.team_abbreviation === selectedTeam);
  };

  return (
    <div className=\"team-matchup-grid\">
      {/* Controls */}
      <div className=\"grid-controls\">
        <div className=\"sort-controls\">
          <label>Sort by:</label>
          <button
            className={`sort-btn ${sortBy === 'points' ? 'active' : ''}`}
            onClick={() => handleSort('points')}
          >
            Fantasy Points {sortBy === 'points' && (sortOrder === 'desc' ? '↓' : '↑')}
          </button>
          <button
            className={`sort-btn ${sortBy === 'team' ? 'active' : ''}`}
            onClick={() => handleSort('team')}
          >
            Team {sortBy === 'team' && (sortOrder === 'desc' ? '↓' : '↑')}
          </button>
        </div>
        
        <div className=\"legend\">
          <span className=\"legend-item excellent\">Excellent</span>
          <span className=\"legend-item good\">Good</span>
          <span className=\"legend-item average\">Average</span>
          <span className=\"legend-item poor\">Poor</span>
        </div>
      </div>

      {/* Team Grid */}
      <div className=\"teams-grid\">
        {sortedResults.map((result) => {
          const colorScore = result.color_score || 0;
          const colorProperties = ColorUtils.generateColorProperties(colorScore);
          const categoryClass = ColorUtils.getCategoryClassName(result.color_category || 'average');
          
          return (
            <div
              key={result.team_abbreviation}
              className={`team-card ${categoryClass} ${selectedTeam === result.team_abbreviation ? 'selected' : ''}`}
              style={colorProperties}
              onClick={() => handleTeamClick(result.team_abbreviation)}
            >
              <div className=\"team-header\">
                <h3 className=\"team-abbr\">{result.team_abbreviation}</h3>
                <div className=\"fantasy-points\">
                  {result.expected_fantasy_points.toFixed(2)}
                </div>
              </div>
              
              <div className=\"team-stats-preview\">
                <div className=\"stat-item\">
                  <span className=\"stat-label\">Hits:</span>
                  <span className=\"stat-value\">{result.expected_hits.toFixed(3)}</span>
                </div>
                <div className=\"stat-item\">
                  <span className=\"stat-label\">HR:</span>
                  <span className=\"stat-value\">{result.expected_home_runs.toFixed(3)}</span>
                </div>
                <div className=\"stat-item\">
                  <span className=\"stat-label\">Runs:</span>
                  <span className=\"stat-value\">{result.expected_runs.toFixed(3)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Detailed View */}
      {selectedTeam && (
        <div className=\"team-details\">
          {(() => {
            const details = getSelectedTeamDetails();
            if (!details) return null;

            return (
              <div className=\"details-card\">
                <div className=\"details-header\">
                  <h3>{details.team_abbreviation} - Detailed Analysis</h3>
                  <button
                    className=\"close-btn\"
                    onClick={() => setSelectedTeam(null)}
                  >
                    ×
                  </button>
                </div>
                
                <div className=\"details-content\">
                  <div className=\"details-section\">
                    <h4>Expected Offensive Stats</h4>
                    <div className=\"stats-grid-detailed\">
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Fantasy Points:</span>
                        <span className=\"value\">{details.expected_fantasy_points.toFixed(2)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Hits:</span>
                        <span className=\"value\">{details.expected_hits.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Singles:</span>
                        <span className=\"value\">{details.expected_singles.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Doubles:</span>
                        <span className=\"value\">{details.expected_doubles.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Triples:</span>
                        <span className=\"value\">{details.expected_triples.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Home Runs:</span>
                        <span className=\"value\">{details.expected_home_runs.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Runs:</span>
                        <span className=\"value\">{details.expected_runs.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">RBI:</span>
                        <span className=\"value\">{details.expected_rbi.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Walks:</span>
                        <span className=\"value\">{details.expected_walks.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">Strikeouts:</span>
                        <span className=\"value\">{details.expected_strikeouts.toFixed(3)}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className=\"details-section\">
                    <h4>Team Pitching Stats (vs {details.handedness})</h4>
                    <div className=\"stats-grid-detailed\">
                      <div className=\"stat-detailed\">
                        <span className=\"label\">ERA:</span>
                        <span className=\"value\">{details.team_stats.era.toFixed(2)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">WHIP:</span>
                        <span className=\"value\">{details.team_stats.whip.toFixed(3)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">K/9:</span>
                        <span className=\"value\">{details.team_stats.k_per_9.toFixed(1)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">BB/9:</span>
                        <span className=\"value\">{details.team_stats.bb_per_9.toFixed(1)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">HR/9:</span>
                        <span className=\"value\">{details.team_stats.hr_per_9.toFixed(2)}</span>
                      </div>
                      <div className=\"stat-detailed\">
                        <span className=\"label\">H/9:</span>
                        <span className=\"value\">{details.team_stats.hits_per_9.toFixed(1)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
};

export default TeamMatchupGrid;

