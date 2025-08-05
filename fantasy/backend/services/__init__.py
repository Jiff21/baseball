"""
Services module - provides both new and legacy service imports for compatibility.
"""

# New services (refactored system)
from .hitting_stats_service import HittingStatsService
from .calculation_service import CalculationService

# Legacy services (imported directly to avoid circular imports)
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class FantasyCalculatorService:
    """Legacy service for calculating fantasy baseball expected points."""
    
    @staticmethod
    def get_scoring_settings(league_type: str) -> Dict:
        """Get scoring settings for a specific league type."""
        # Import here to avoid circular imports
        try:
            from models import ScoringSettings
            if league_type.upper() == 'ESPN':
                return ScoringSettings.get_espn_settings()
            elif league_type.upper() == 'CBS':
                return ScoringSettings.get_cbs_settings()
            elif league_type.upper() == 'YAHOO':
                return ScoringSettings.get_yahoo_settings()
            else:
                return ScoringSettings.get_default_settings()
        except ImportError:
            # Fallback to basic settings
            return {
                'batting': {'HR': 4, 'R': 1, 'RBI': 1, 'SB': 2, 'BB': 1},
                'pitching': {'W': 5, 'K': 1, 'S': 5, 'ER': -1, 'BB': -1}
            }
    
    @staticmethod
    def calculate_expected_points(
        team_abbreviation: str,
        handedness: str,
        inning: int,
        scoring_settings: Dict
    ) -> Dict:
        """Calculate expected fantasy points for a team matchup."""
        # Basic implementation for compatibility
        return {
            'team_abbreviation': team_abbreviation,
            'handedness': handedness,
            'inning': inning,
            'expected_fantasy_points': 0.0,
            'expected_runs': 0.0,
            'expected_hits': 0.0,
            'expected_home_runs': 0.0,
            'expected_strikeouts': 0.0,
            'expected_walks': 0.0
        }


class TeamService:
    """Legacy service for team-related operations."""
    
    @staticmethod
    def get_all_teams() -> List[Dict]:
        """Get all teams with their statistics."""
        try:
            from models import Team
            teams = Team.query.all()
            return [team.to_dict() for team in teams]
        except ImportError:
            return []
    
    @staticmethod
    def get_team_by_abbreviation(abbreviation: str) -> Optional[Dict]:
        """Get a specific team by abbreviation."""
        try:
            from models import Team
            team = Team.query.filter_by(abbreviation=abbreviation.upper()).first()
            return team.to_dict() if team else None
        except ImportError:
            return None


# Export all services
__all__ = [
    'HittingStatsService',
    'CalculationService', 
    'FantasyCalculatorService',
    'TeamService'
]
