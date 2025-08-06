/**
 * Tests for FantasyExpectedStart component
 */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import FantasyExpectedStart from '../FantasyExpectedStart';
import { FantasyBaseballAPI } from '../../services/api';

// Mock the API
jest.mock('../../services/api');
const mockAPI = FantasyBaseballAPI as jest.Mocked<typeof FantasyBaseballAPI>;

// Mock localStorage
const mockLocalStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

describe('FantasyExpectedStart', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.getItem.mockReturnValue(null);
    
    // Mock API responses
    mockAPI.getScoringSettings.mockResolvedValue({
      data: {
        league_type: 'Custom',
        scoring_settings: {
          batting: {
            S: 1, D: 2, T: 3, HR: 4, BB: 1, IBB: 1, HBP: 1,
            R: 1, RBI: 1, SB: 2, CS: -1, SO: -1, GIDP: 0, E: 0
          },
          pitching: {
            BB: -1, IBB: -1, ER: -1, HA: -1, HB: -1, HRA: -3,
            INN: 3, K: 1, W: 5, L: -3, S: 5, BS: 0, QS: 0,
            TB: 0, Hold: 0, WP: 0, BK: 0
          }
        }
      }
    });
  });

  test('renders main components', () => {
    render(<FantasyExpectedStart />);
    
    expect(screen.getByText('Fantasy Expected Start')).toBeInTheDocument();
    expect(screen.getByLabelText(/Pitcher Handedness/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/League Type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Innings/i)).toBeInTheDocument();
    expect(screen.getByText('Calculate Expected Points')).toBeInTheDocument();
  });

  test('has correct default values', () => {
    render(<FantasyExpectedStart />);
    
    const handednessSelect = screen.getByLabelText(/Pitcher Handedness/i) as HTMLSelectElement;
    const leagueSelect = screen.getByLabelText(/League Type/i) as HTMLSelectElement;
    const inningInput = screen.getByLabelText(/Innings/i) as HTMLInputElement;
    
    expect(handednessSelect.value).toBe('Righty');
    expect(leagueSelect.value).toBe('Custom');
    expect(inningInput.value).toBe('6');
  });

  test('changes handedness selection', () => {
    render(<FantasyExpectedStart />);
    
    const handednessSelect = screen.getByLabelText(/Pitcher Handedness/i) as HTMLSelectElement;
    
    fireEvent.change(handednessSelect, { target: { value: 'Lefty' } });
    expect(handednessSelect.value).toBe('Lefty');
  });

  test('changes league type selection', () => {
    render(<FantasyExpectedStart />);
    
    const leagueSelect = screen.getByLabelText(/League Type/i) as HTMLSelectElement;
    
    fireEvent.change(leagueSelect, { target: { value: 'ESPN' } });
    expect(leagueSelect.value).toBe('ESPN');
  });

  test('validates inning input', () => {
    render(<FantasyExpectedStart />);
    
    const inningInput = screen.getByLabelText(/Innings/i) as HTMLInputElement;
    
    // Valid input
    fireEvent.change(inningInput, { target: { value: '9' } });
    expect(inningInput.value).toBe('9');
    
    // Invalid input (too high) - should not change
    fireEvent.change(inningInput, { target: { value: '10' } });
    expect(inningInput.value).toBe('9');
    
    // Invalid input (too low) - should not change
    fireEvent.change(inningInput, { target: { value: '0' } });
    expect(inningInput.value).toBe('9');
  });

  test('shows scoring settings for custom league', async () => {
    render(<FantasyExpectedStart />);
    
    await waitFor(() => {
      expect(screen.getByText(/Custom Scoring Settings/i)).toBeInTheDocument();
    });
    
    expect(screen.getByText('Batting')).toBeInTheDocument();
    expect(screen.getByText('Pitching')).toBeInTheDocument();
  });

  test('shows league name input for custom league', async () => {
    render(<FantasyExpectedStart />);
    
    await waitFor(() => {
      expect(screen.getByLabelText(/League Name/i)).toBeInTheDocument();
      expect(screen.getByText('Save')).toBeInTheDocument();
    });
  });

  test('calculate button calls API', async () => {
    mockAPI.calculateExpected.mockResolvedValue({
      data: {
        results: [
          {
            team_abbreviation: 'LAD',
            handedness: 'Righty',
            inning: 6,
            expected_fantasy_points: 5.5,
            expected_runs: 1.2,
            expected_hits: 2.1,
            expected_singles: 1.5,
            expected_doubles: 0.4,
            expected_triples: 0.1,
            expected_home_runs: 0.1,
            expected_walks: 0.8,
            expected_strikeouts: 1.5,
            expected_rbi: 1.2,
            team_stats: {
              era: 3.50,
              whip: 1.20,
              k_per_9: 9.0,
              bb_per_9: 3.0,
              hr_per_9: 1.0,
              hits_per_9: 8.0
            },
            color_score: 0.7,
            color_category: 'good' as const
          }
        ],
        analysis: {
          min_points: 5.5,
          max_points: 5.5,
          avg_points: 5.5,
          total_teams: 1
        },
        parameters: {
          handedness: 'Righty',
          inning: 6,
          league_type: 'Custom'
        }
      }
    });

    render(<FantasyExpectedStart />);
    
    await waitFor(() => {
      expect(screen.getByText('Calculate Expected Points')).toBeInTheDocument();
    });

    const calculateButton = screen.getByText('Calculate Expected Points');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(mockAPI.calculateExpected).toHaveBeenCalledWith({
        handedness: 'Righty',
        inning: 6,
        league_type: 'Custom',
        custom_scoring: expect.any(Object)
      });
    });
  });

  test('displays error message on API failure', async () => {
    mockAPI.calculateExpected.mockResolvedValue({
      error: 'API Error'
    });

    render(<FantasyExpectedStart />);
    
    await waitFor(() => {
      expect(screen.getByText('Calculate Expected Points')).toBeInTheDocument();
    });

    const calculateButton = screen.getByText('Calculate Expected Points');
    fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByText('API Error')).toBeInTheDocument();
    });
  });

  test('shows loading state during calculation', async () => {
    // Mock a delayed response
    mockAPI.calculateExpected.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({ data: {} as any }), 100))
    );

    render(<FantasyExpectedStart />);
    
    await waitFor(() => {
      expect(screen.getByText('Calculate Expected Points')).toBeInTheDocument();
    });

    const calculateButton = screen.getByText('Calculate Expected Points');
    fireEvent.click(calculateButton);

    expect(screen.getByText('Calculating...')).toBeInTheDocument();
    expect(calculateButton).toBeDisabled();
  });
});
