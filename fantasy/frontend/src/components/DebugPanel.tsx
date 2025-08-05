/**
 * Debug Panel component for exporting raw data and calculated stats to CSV
 */
import React, { useState } from 'react';
import './DebugPanel.css';

interface DebugPanelProps {
  apiBaseUrl?: string;
}

const DebugPanel: React.FC<DebugPanelProps> = ({ 
  apiBaseUrl = 'http://localhost:8000' 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string>('');
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('');

  const showMessage = (text: string, type: 'success' | 'error') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => {
      setMessage('');
      setMessageType('');
    }, 5000);
  };

  const handleFetchHittingStats = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/fetch-hitting-stats`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          season: new Date().getFullYear()
        })
      });

      const data = await response.json();
      
      if (data.success) {
        showMessage(
          `Successfully fetched and stored hitting stats for ${data.stored_teams} team-split combinations`,
          'success'
        );
      } else {
        showMessage(`Error: ${data.error}`, 'error');
      }
    } catch (error) {
      showMessage(`Network error: ${error}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportRawStats = async () => {
    setIsLoading(true);
    try {
      const currentYear = new Date().getFullYear();
      const response = await fetch(`${apiBaseUrl}/api/debug/raw-stats-csv?season=${currentYear}`);
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `raw_hitting_stats_${currentYear}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showMessage('Raw hitting stats CSV downloaded successfully', 'success');
      } else {
        const errorData = await response.json();
        showMessage(`Error: ${errorData.error}`, 'error');
      }
    } catch (error) {
      showMessage(`Network error: ${error}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportCalculatedStats = async () => {
    setIsLoading(true);
    try {
      const currentYear = new Date().getFullYear();
      const response = await fetch(`${apiBaseUrl}/api/debug/calculated-stats-csv?season=${currentYear}`);
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `calculated_stats_${currentYear}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showMessage('Calculated stats CSV downloaded successfully', 'success');
      } else {
        const errorData = await response.json();
        showMessage(`Error: ${errorData.error}`, 'error');
      }
    } catch (error) {
      showMessage(`Network error: ${error}`, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="debug-panel">
      <div className="debug-panel-header">
        <h3>Debug Panel</h3>
        <p>Tools for debugging and data export</p>
      </div>

      {message && (
        <div className={`debug-message ${messageType}`}>
          {message}
        </div>
      )}

      <div className="debug-actions">
        <div className="debug-section">
          <h4>Data Management</h4>
          <button
            className="debug-button primary"
            onClick={handleFetchHittingStats}
            disabled={isLoading}
          >
            {isLoading ? 'Fetching...' : 'Fetch Hitting Stats from MLB APIs'}
          </button>
          <p className="debug-description">
            Fetches hitting statistics from all three MLB APIs (lefty, righty, overall splits) 
            and stores them in the database with calculated per-PA rates.
          </p>
        </div>

        <div className="debug-section">
          <h4>Data Export</h4>
          <div className="debug-button-group">
            <button
              className="debug-button secondary"
              onClick={handleExportRawStats}
              disabled={isLoading}
            >
              {isLoading ? 'Exporting...' : 'Export Raw Stats CSV'}
            </button>
            <button
              className="debug-button secondary"
              onClick={handleExportCalculatedStats}
              disabled={isLoading}
            >
              {isLoading ? 'Exporting...' : 'Export Calculated Stats CSV'}
            </button>
          </div>
          <p className="debug-description">
            Export raw hitting statistics or calculated per-PA rates to CSV files 
            for debugging and analysis purposes.
          </p>
        </div>
      </div>

      <div className="debug-info">
        <h4>Debug Information</h4>
        <div className="debug-info-grid">
          <div className="debug-info-item">
            <strong>Raw Stats CSV includes:</strong>
            <ul>
              <li>Team abbreviation and name</li>
              <li>Split type (lefty, righty, overall)</li>
              <li>Games, plate appearances, at bats</li>
              <li>Hits breakdown (singles, doubles, triples, HR)</li>
              <li>Walks, strikeouts, stolen bases</li>
              <li>Wins and losses by split</li>
            </ul>
          </div>
          <div className="debug-info-item">
            <strong>Calculated Stats CSV includes:</strong>
            <ul>
              <li>Per-PA rates for all hitting stats</li>
              <li>Plate appearances per inning</li>
              <li>Wins/losses per game</li>
              <li>All rates used for expected calculations</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DebugPanel;
