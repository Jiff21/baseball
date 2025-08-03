/**
 * API service for communicating with the Fantasy Baseball backend.
 */
import axios, { AxiosResponse } from 'axios';
import {
  ScoringSettings,
  Team,
  MatchupAnalysisResult,
  CalculateExpectedRequest,
  ApiResponse
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export class FantasyBaseballAPI {
  /**
   * Health check endpoint
   */
  static async healthCheck(): Promise<ApiResponse<{ status: string; message: string }>> {
    try {
      const response: AxiosResponse = await apiClient.get('/health');
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Health check failed' };
    }
  }

  /**
   * Get scoring settings for a specific league type
   */
  static async getScoringSettings(leagueType: string): Promise<ApiResponse<{
    league_type: string;
    scoring_settings: ScoringSettings;
  }>> {
    try {
      const response: AxiosResponse = await apiClient.get(`/scoring-settings/${leagueType}`);
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Failed to get scoring settings' };
    }
  }

  /**
   * Get all teams
   */
  static async getTeams(): Promise<ApiResponse<{ teams: Team[]; count: number }>> {
    try {
      const response: AxiosResponse = await apiClient.get('/teams');
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Failed to get teams' };
    }
  }

  /**
   * Get team stats for all teams (vs lefty and righty)
   */
  static async getTeamStats(): Promise<ApiResponse<{ teams: any[]; count: number }>> {
    try {
      const response: AxiosResponse = await apiClient.get('/team-stats');
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Failed to get team stats' };
    }
  }

  /**
   * Get a specific team by abbreviation
   */
  static async getTeam(abbreviation: string): Promise<ApiResponse<{ team: Team }>> {
    try {
      const response: AxiosResponse = await apiClient.get(`/teams/${abbreviation}`);
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Failed to get team' };
    }
  }

  /**
   * Calculate expected fantasy points for all teams
   */
  static async calculateExpected(
    request: CalculateExpectedRequest
  ): Promise<ApiResponse<MatchupAnalysisResult>> {
    try {
      const response: AxiosResponse = await apiClient.post('/matchup-analysis', request);
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Failed to calculate expected points' };
    }
  }

  /**
   * Calculate expected fantasy points for a specific team
   */
  static async calculateTeamExpected(
    teamAbbreviation: string,
    handedness: string,
    inning: number,
    leagueType: string,
    customScoring?: ScoringSettings
  ): Promise<ApiResponse<any>> {
    try {
      const request = {
        team_abbreviation: teamAbbreviation,
        handedness,
        inning,
        league_type: leagueType,
        ...(customScoring && { custom_scoring: customScoring }),
      };

      const response: AxiosResponse = await apiClient.post('/calculate-team-expected', request);
      return { data: response.data };
    } catch (error: any) {
      return { error: error.response?.data?.error || 'Failed to calculate team expected points' };
    }
  }
}

export default FantasyBaseballAPI;
