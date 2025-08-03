import React, { useState, useEffect } from 'react';

interface ScoringSettings {
  // Batting
  singles: number;
  doubles: number;
  triples: number;
  homeRuns: number;
  walks: number;
  intentionalWalks: number;
  hitByPitch: number;
  runs: number;
  runsBattedIn: number;
  stolenBase: number;
  caughtStealing: number;
  strikeOuts: number;
  
  // Pitching
  walksIssued: number;
  intentionalBaseOnBalls: number;
  earnedRuns: number;
  hitsAllowed: number;
  hitBatters: number;
  homeRunsAllowed: number;
  innings: number;
  strikeouts: number;
  wins: number;
  losses: number;
  saves: number;
  blownSaves: number;
  qualityStarts: number;
  totalBases: number;
}

type LeagueType = 'custom' | 'espn' | 'cbs' | 'yahoo';

const FantasyExpectedStart: React.FC = () => {
  const [leagueType, setLeagueType] = useState<LeagueType>('custom');
  const [scoringSettings, setScoringSettings] = useState<ScoringSettings>({
    // Default custom values
    singles: 1.0,
    doubles: 2.0,
    triples: 3.0,
    homeRuns: 4.0,
    walks: 1.0,
    intentionalWalks: 1.0,
    hitByPitch: 1.0,
    runs: 1.0,
    runsBattedIn: 1.0,
    stolenBase: 1.0,
    caughtStealing: -1.0,
    strikeOuts: 0.5,
    walksIssued: -1.0,
    intentionalBaseOnBalls: -1.0,
    earnedRuns: -1.0,
    hitsAllowed: -1.0,
    hitBatters: -1.0,
    homeRunsAllowed: -1.0,
    innings: 3.0,
    strikeouts: 0.5,
    wins: 2.0,
    losses: -1.0,
    saves: 2.0,
    blownSaves: -1.0,
    qualityStarts: 2.0,
    totalBases: 0.0
  });

  const getLeagueSettings = (league: LeagueType): ScoringSettings => {
    switch (league) {
      case 'custom':
        return {
          singles: 1.0,
          doubles: 2.0,
          triples: 3.0,
          homeRuns: 4.0,
          walks: 1.0,
          intentionalWalks: 1.0,
          hitByPitch: 1.0,
          runs: 1.0,
          runsBattedIn: 1.0,
          stolenBase: 1.0,
          caughtStealing: -1.0,
          strikeOuts: 0.5,
          walksIssued: -1.0,
          intentionalBaseOnBalls: -1.0,
          earnedRuns: -1.0,
          hitsAllowed: -1.0,
          hitBatters: -1.0,
          homeRunsAllowed: -1.0,
          innings: 3.0,
          strikeouts: 0.5,
          wins: 2.0,
          losses: -1.0,
          saves: 2.0,
          blownSaves: -1.0,
          qualityStarts: 2.0,
          totalBases: 0.0
        };
      case 'espn':
        return {
          singles: 1.0,
          doubles: 2.0,
          triples: 3.0,
          homeRuns: 4.0,
          walks: 1.0,
          intentionalWalks: 0.0,
          hitByPitch: 0.0,
          runs: 1.0,
          runsBattedIn: 1.0,
          stolenBase: 1.0,
          caughtStealing: 0.0,
          strikeOuts: -1.0,
          walksIssued: -1.0,
          intentionalBaseOnBalls: -1.0,
          earnedRuns: -1.0,
          hitsAllowed: -1.0,
          hitBatters: 0.0,
          homeRunsAllowed: -1.0,
          innings: 3.0,
          strikeouts: 1.0,
          wins: 2.0,
          losses: -1.0,
          saves: 2.0,
          blownSaves: 0.0,
          qualityStarts: 0.0,
          totalBases: 0.0
        };
      case 'cbs':
        return {
          singles: 1.0,
          doubles: 2.0,
          triples: 3.0,
          homeRuns: 4.0,
          walks: 1.0,
          intentionalWalks: 1.0,
          hitByPitch: 1.0,
          runs: 1.0,
          runsBattedIn: 1.0,
          stolenBase: 2.0,
          caughtStealing: -1.0,
          strikeOuts: -1.0,
          walksIssued: -1.0,
          intentionalBaseOnBalls: -1.0,
          earnedRuns: -1.0,
          hitsAllowed: -1.0,
          hitBatters: 0.0,
          homeRunsAllowed: -1.0,
          innings: 3.0,
          strikeouts: 1.0,
          wins: 5.0,
          losses: -3.0,
          saves: 2.0,
          blownSaves: -2.0,
          qualityStarts: 0.0,
          totalBases: 0.0
        };
      case 'yahoo':
        return {
          singles: 1.0,
          doubles: 2.0,
          triples: 3.0,
          homeRuns: 4.0,
          walks: 1.0,
          intentionalWalks: 1.0,
          hitByPitch: 1.0,
          runs: 1.0,
          runsBattedIn: 1.0,
          stolenBase: 2.0,
          caughtStealing: -1.0,
          strikeOuts: -1.0,
          walksIssued: -1.0,
          intentionalBaseOnBalls: -1.0,
          earnedRuns: -1.0,
          hitsAllowed: -1.0,
          hitBatters: 0.0,
          homeRunsAllowed: -1.0,
          innings: 3.0,
          strikeouts: 1.0,
          wins: 5.0,
          losses: -3.0,
          saves: 2.0,
          blownSaves: -2.0,
          qualityStarts: 0.0,
          totalBases: 0.0
        };
      default:
        return getLeagueSettings('custom');
    }
  };

  useEffect(() => {
    setScoringSettings(getLeagueSettings(leagueType));
  }, [leagueType]);

  const handleLeagueTypeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setLeagueType(event.target.value as LeagueType);
  };

  const handleSettingChange = (field: keyof ScoringSettings, value: number) => {
    setScoringSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getValueColor = (value: number): string => {
    if (value > 0) return '#27ae60'; // Green for positive
    if (value < 0) return '#e74c3c'; // Red for negative
    return '#7f8c8d'; // Gray for zero
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Existing dropdown - placeholder for whatever was there before */}
      <div style={{ marginBottom: '30px' }}>
        <label htmlFor="leagueType" style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
          League Type:
        </label>
        <select
          id="leagueType"
          value={leagueType}
          onChange={handleLeagueTypeChange}
          style={{
            padding: '8px 12px',
            fontSize: '16px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            backgroundColor: 'white'
          }}
        >
          <option value="custom">Custom</option>
          <option value="espn">ESPN</option>
          <option value="cbs">CBS</option>
          <option value="yahoo">Yahoo</option>
        </select>
      </div>

      {/* Scoring Settings Section */}
      <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h2 style={{ color: '#2c3e50', marginBottom: '30px', borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>
          Scoring Settings
        </h2>

        {/* Batting Section */}
        <div style={{ marginBottom: '40px' }}>
          <h3 style={{ color: '#34495e', marginBottom: '20px' }}>Batting</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px' }}>
            {[
              { key: 'singles', label: 'Singles' },
              { key: 'doubles', label: 'Doubles' },
              { key: 'triples', label: 'Triples' },
              { key: 'homeRuns', label: 'Home Runs' },
              { key: 'walks', label: 'Walks' },
              { key: 'intentionalWalks', label: 'Intentional Walks' },
              { key: 'hitByPitch', label: 'Hit By Pitch' },
              { key: 'runs', label: 'Runs' },
              { key: 'runsBattedIn', label: 'Runs Batted In' },
              { key: 'stolenBase', label: 'Stolen Base' },
              { key: 'caughtStealing', label: 'Caught Stealing' },
              { key: 'strikeOuts', label: 'Strike Outs' }
            ].map(({ key, label }) => (
              <div key={key} style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '12px',
                backgroundColor: '#f8f9fa',
                borderRadius: '5px',
                borderLeft: '4px solid #3498db'
              }}>
                <span style={{ fontWeight: 'bold', color: '#2c3e50' }}>{label}:</span>
                <input
                  type="number"
                  step="0.1"
                  value={scoringSettings[key as keyof ScoringSettings]}
                  onChange={(e) => handleSettingChange(key as keyof ScoringSettings, parseFloat(e.target.value) || 0)}
                  style={{
                    width: '80px',
                    padding: '6px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    textAlign: 'center',
                    color: getValueColor(scoringSettings[key as keyof ScoringSettings])
                  }}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Pitching Section */}
        <div>
          <h3 style={{ color: '#34495e', marginBottom: '20px' }}>Pitching</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px' }}>
            {[
              { key: 'walksIssued', label: 'Walks Issued' },
              { key: 'intentionalBaseOnBalls', label: 'Intentional Base on Balls' },
              { key: 'earnedRuns', label: 'Earned Runs' },
              { key: 'hitsAllowed', label: 'Hits allowed' },
              { key: 'hitBatters', label: 'Hit Batters' },
              { key: 'homeRunsAllowed', label: 'Home Runs Allowed' },
              { key: 'innings', label: 'Innings' },
              { key: 'strikeouts', label: 'Strikeouts' },
              { key: 'wins', label: 'Wins' },
              { key: 'losses', label: 'Losses' },
              { key: 'saves', label: 'Saves' },
              { key: 'blownSaves', label: 'Blown Saves' },
              { key: 'qualityStarts', label: 'Quality Starts' },
              { key: 'totalBases', label: 'Total Bases' }
            ].map(({ key, label }) => (
              <div key={key} style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '12px',
                backgroundColor: '#f8f9fa',
                borderRadius: '5px',
                borderLeft: '4px solid #3498db'
              }}>
                <span style={{ fontWeight: 'bold', color: '#2c3e50' }}>{label}:</span>
                <input
                  type="number"
                  step="0.1"
                  value={scoringSettings[key as keyof ScoringSettings]}
                  onChange={(e) => handleSettingChange(key as keyof ScoringSettings, parseFloat(e.target.value) || 0)}
                  style={{
                    width: '80px',
                    padding: '6px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    textAlign: 'center',
                    color: getValueColor(scoringSettings[key as keyof ScoringSettings])
                  }}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Legend */}
        <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#ecf0f1', borderRadius: '5px' }}>
          <h4 style={{ marginBottom: '10px' }}>Scoring Legend:</h4>
          <p style={{ margin: '5px 0' }}>
            <span style={{ color: '#27ae60', fontWeight: 'bold' }}>Green values</span> indicate positive scoring (points awarded)
          </p>
          <p style={{ margin: '5px 0' }}>
            <span style={{ color: '#e74c3c', fontWeight: 'bold' }}>Red values</span> indicate negative scoring (points deducted)
          </p>
          <p style={{ margin: '5px 0' }}>
            <span style={{ color: '#7f8c8d', fontWeight: 'bold' }}>Gray values</span> indicate neutral scoring (no points)
          </p>
        </div>
      </div>
    </div>
  );
};

export default FantasyExpectedStart;
