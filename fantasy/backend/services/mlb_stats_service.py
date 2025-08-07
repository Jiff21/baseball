"""
MLB Statistics Service for extracting team data from MLB API
"""
import requests
import json
from typing import Dict, Optional, Any


class MLBStatsExtractor:
    """Service class to extract team statistics from MLB standings data"""
    
    def __init__(self, standings_url: str = None):
        """
        Initialize the MLB Stats Extractor
        
        Args:
            standings_url: URL to fetch MLB standings data from
        """
        self.standings_url = standings_url or "https://statsapi.mlb.com/api/v1/standings"
        self.standings_data = None
    
    def fetch_standings_data(self) -> Dict[str, Any]:
        """
        Fetch standings data from MLB API
        
        Returns:
            Dict containing MLB standings data
            
        Raises:
            requests.RequestException: If API request fails
        """
        try:
            response = requests.get(self.standings_url, timeout=30)
            response.raise_for_status()
            self.standings_data = response.json()
            return self.standings_data
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch MLB standings data: {e}")
    
    def load_standings_data(self, data: Dict[str, Any]) -> None:
        """
        Load standings data from a dictionary (useful for testing)
        
        Args:
            data: Dictionary containing MLB standings data
        """
        self.standings_data = data
    
    def find_team_record(self, team_abbreviation: str) -> Optional[Dict[str, Any]]:
        """
        Find team record by abbreviation
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Dictionary containing team record data or None if not found
        """
        if not self.standings_data:
            return None
            
        for record in self.standings_data.get('records', []):
            for team_record in record.get('teamRecords', []):
                if team_record.get('abbreviation') == team_abbreviation:
                    return team_record
        return None
    
    def get_wins_against_righties(self, team_abbreviation: str) -> int:
        """
        Extract wins against right-handed pitching
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Number of wins against right-handed pitching
        """
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_right field (format: "wins-losses")
            record_right = team_record.get('record_right', '0-0')
            wins = int(record_right.split('-')[0])
            return wins
        return 0
    
    def get_losses_against_righties(self, team_abbreviation: str) -> int:
        """
        Extract losses against right-handed pitching
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Number of losses against right-handed pitching
        """
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_right field (format: "wins-losses")
            record_right = team_record.get('record_right', '0-0')
            losses = int(record_right.split('-')[1])
            return losses
        return 0
    
    def get_wins_against_lefties(self, team_abbreviation: str) -> int:
        """
        Extract wins against left-handed pitching
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Number of wins against left-handed pitching
        """
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_left field (format: "wins-losses")
            record_left = team_record.get('record_left', '0-0')
            wins = int(record_left.split('-')[0])
            return wins
        return 0
    
    def get_losses_against_lefties(self, team_abbreviation: str) -> int:
        """
        Extract losses against left-handed pitching
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Number of losses against left-handed pitching
        """
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_left field (format: "wins-losses")
            record_left = team_record.get('record_left', '0-0')
            losses = int(record_left.split('-')[1])
            return losses
        return 0
    
    def get_total_wins(self, team_abbreviation: str) -> int:
        """
        Extract total wins (no splits)
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Total number of wins
        """
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            return team_record.get('wins', 0)
        return 0
    
    def get_total_losses(self, team_abbreviation: str) -> int:
        """
        Extract total losses (no splits)
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Total number of losses
        """
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            return team_record.get('losses', 0)
        return 0
    
    def get_team_stats_summary(self, team_abbreviation: str) -> Dict[str, int]:
        """
        Get a complete summary of team statistics
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'SF', 'NYY')
            
        Returns:
            Dictionary containing all team statistics
        """
        return {
            'total_wins': self.get_total_wins(team_abbreviation),
            'total_losses': self.get_total_losses(team_abbreviation),
            'wins_vs_righties': self.get_wins_against_righties(team_abbreviation),
            'losses_vs_righties': self.get_losses_against_righties(team_abbreviation),
            'wins_vs_lefties': self.get_wins_against_lefties(team_abbreviation),
            'losses_vs_lefties': self.get_losses_against_lefties(team_abbreviation)
        }
