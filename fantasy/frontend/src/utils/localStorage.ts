/**
 * Utility functions for managing localStorage operations.
 */
import { CustomLeague, ScoringSettings } from '../types';

const CUSTOM_LEAGUES_KEY = 'fantasy_baseball_custom_leagues';

export class LocalStorageManager {
  /**
   * Save a custom league to localStorage
   */
  static saveCustomLeague(league: CustomLeague): void {
    try {
      const existingLeagues = this.getCustomLeagues();
      
      // Check if league with same name exists
      const existingIndex = existingLeagues.findIndex(l => l.name === league.name);
      
      if (existingIndex >= 0) {
        // Update existing league
        existingLeagues[existingIndex] = league;
      } else {
        // Add new league
        existingLeagues.push(league);
      }
      
      localStorage.setItem(CUSTOM_LEAGUES_KEY, JSON.stringify(existingLeagues));
    } catch (error) {
      console.error('Error saving custom league:', error);
    }
  }

  /**
   * Get all custom leagues from localStorage
   */
  static getCustomLeagues(): CustomLeague[] {
    try {
      const stored = localStorage.getItem(CUSTOM_LEAGUES_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Error getting custom leagues:', error);
      return [];
    }
  }

  /**
   * Get a specific custom league by name
   */
  static getCustomLeague(name: string): CustomLeague | null {
    try {
      const leagues = this.getCustomLeagues();
      return leagues.find(l => l.name === name) || null;
    } catch (error) {
      console.error('Error getting custom league:', error);
      return null;
    }
  }

  /**
   * Delete a custom league
   */
  static deleteCustomLeague(name: string): void {
    try {
      const leagues = this.getCustomLeagues();
      const filtered = leagues.filter(l => l.name !== name);
      localStorage.setItem(CUSTOM_LEAGUES_KEY, JSON.stringify(filtered));
    } catch (error) {
      console.error('Error deleting custom league:', error);
    }
  }

  /**
   * Clear all custom leagues
   */
  static clearCustomLeagues(): void {
    try {
      localStorage.removeItem(CUSTOM_LEAGUES_KEY);
    } catch (error) {
      console.error('Error clearing custom leagues:', error);
    }
  }

  /**
   * Get custom league names for dropdown
   */
  static getCustomLeagueNames(): string[] {
    try {
      const leagues = this.getCustomLeagues();
      return leagues.map(l => l.name);
    } catch (error) {
      console.error('Error getting custom league names:', error);
      return [];
    }
  }
}

export default LocalStorageManager;

