"""
Business logic services for the Fantasy Baseball application.
"""
import logging
from typing import Dict, List, Optional
from models import db, Team, ExpectedGame, ScoringSettings

logger = logging.getLogger(__name__)


class FantasyCalculatorService:
    """Service for calculating fantasy baseball expected points."""
    
    @staticmethod
    def get_scoring_settings(league_type: str) -> Dict:
        """
        Get scoring settings for a specific league type.
        
        Args:
            league_type: Type of league ('Custom', 'ESPN', 'CBS', 'Yahoo')
            
        Returns:
            Dictionary containing scoring settings
        """
        if league_type.upper() == 'ESPN':
            return ScoringSettings.get_espn_settings()
        elif league_type.upper() == 'CBS':
            return ScoringSettings.get_cbs_settings()
        elif league_type.upper() == 'YAHOO':
            return ScoringSettings.get_yahoo_settings()
        else:
            return ScoringSettings.get_default_settings()
    
    @staticmethod
    def calculate_expected_points(
        team_abbreviation: str,
        handedness: str,
        inning: int,
        scoring_settings: Dict
    ) -> Dict:
        """
        Calculate expected fantasy points for a team matchup.
        
        Args:
            team_abbreviation: Team abbreviation (e.g., 'LAD')
            handedness: Batter handedness ('Lefty' or 'Righty')
            inning: Number of innings to calculate for (1-9)
            scoring_settings: Dictionary of scoring settings
            
        Returns:
            Dictionary containing expected statistics and points
        """
        # Get team data
        team = Team.query.filter_by(abbreviation=team_abbreviation).first()
        if not team:
            raise ValueError(f"Team {team_abbreviation} not found")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"CALCULATING EXPECTED POINTS FOR {team.name} ({team_abbreviation})")
        logger.info(f"Handedness: {handedness} | Innings: {inning}")
        logger.info(f"{'='*60}")
        
        # Select appropriate stats based on handedness
        if handedness.lower() == 'lefty':
            era = team.vs_lefty_era
            whip = team.vs_lefty_whip
            k_per_9 = team.vs_lefty_k_per_9
            bb_per_9 = team.vs_lefty_bb_per_9
            hr_per_9 = team.vs_lefty_hr_per_9
            hits_per_9 = team.vs_lefty_hits_per_9
            
            logger.info(f"📊 RAW TEAM STATS vs LEFTIES:")
            logger.info(f"   ERA: {era}")
            logger.info(f"   WHIP: {whip}")
            logger.info(f"   K/9: {k_per_9}")
            logger.info(f"   BB/9: {bb_per_9}")
            logger.info(f"   HR/9: {hr_per_9}")
            logger.info(f"   Hits/9: {hits_per_9}")
            logger.info(f"   ⚠️  NOTE: Wins/Losses vs lefties not available in database model")
        else:
            era = team.vs_righty_era
            whip = team.vs_righty_whip
            k_per_9 = team.vs_righty_k_per_9
            bb_per_9 = team.vs_righty_bb_per_9
            hr_per_9 = team.vs_righty_hr_per_9
            hits_per_9 = team.vs_righty_hits_per_9
            
            logger.info(f"📊 RAW TEAM STATS vs RIGHTIES:")
            logger.info(f"   ERA: {era}")
            logger.info(f"   WHIP: {whip}")
            logger.info(f"   K/9: {k_per_9}")
            logger.info(f"   BB/9: {bb_per_9}")
            logger.info(f"   HR/9: {hr_per_9}")
            logger.info(f"   Hits/9: {hits_per_9}")
            logger.info(f"   ⚠️  NOTE: Wins/Losses vs righties not available in database model")
        
        # Calculate expected stats per inning
        innings_factor = inning / 9.0
        
        logger.info(f"\n🧮 PER_9 CALCULATIONS:")
        logger.info(f"   Innings Factor: {inning}/9 = {innings_factor:.4f}")
        
        # Basic expected stats (simplified calculation)
        expected_hits = (hits_per_9 * innings_factor) / 9  # Per batter
        expected_walks = (bb_per_9 * innings_factor) / 9
        expected_strikeouts = (k_per_9 * innings_factor) / 9
        expected_home_runs = (hr_per_9 * innings_factor) / 9
        expected_runs = (era * innings_factor) / 9
        
        logger.info(f"   Expected Hits: ({hits_per_9} * {innings_factor:.4f}) / 9 = {expected_hits:.6f}")
        logger.info(f"   Expected Walks: ({bb_per_9} * {innings_factor:.4f}) / 9 = {expected_walks:.6f}")
        logger.info(f"   Expected Strikeouts: ({k_per_9} * {innings_factor:.4f}) / 9 = {expected_strikeouts:.6f}")
        logger.info(f"   Expected Home Runs: ({hr_per_9} * {innings_factor:.4f}) / 9 = {expected_home_runs:.6f}")
        logger.info(f"   Expected Runs: ({era} * {innings_factor:.4f}) / 9 = {expected_runs:.6f}")
        
        # Break down hits into singles, doubles, triples
        # Typical distribution: ~75% singles, ~20% doubles, ~3% triples, ~2% HR
        expected_singles = expected_hits * 0.75
        expected_doubles = expected_hits * 0.20
        expected_triples = expected_hits * 0.03
        
        logger.info(f"\n⚾ HIT BREAKDOWN (Distribution):")
        logger.info(f"   Expected Singles: {expected_hits:.6f} * 0.75 = {expected_singles:.6f}")
        logger.info(f"   Expected Doubles: {expected_hits:.6f} * 0.20 = {expected_doubles:.6f}")
        logger.info(f"   Expected Triples: {expected_hits:.6f} * 0.03 = {expected_triples:.6f}")
        logger.info(f"   Expected Home Runs: {expected_home_runs:.6f} (from HR/9 stat)")
        
        # Calculate fantasy points
        singles_points = expected_singles * scoring_settings['batting'].get('S', 0)
        doubles_points = expected_doubles * scoring_settings['batting'].get('D', 0)
        triples_points = expected_triples * scoring_settings['batting'].get('T', 0)
        hr_points = expected_home_runs * scoring_settings['batting'].get('HR', 0)
        walks_points = expected_walks * scoring_settings['batting'].get('BB', 0)
        runs_points = expected_runs * scoring_settings['batting'].get('R', 0)
        strikeouts_points = expected_strikeouts * scoring_settings['batting'].get('SO', 0)
        
        # For simplicity, assume RBI roughly equals runs
        expected_rbi = expected_runs
        rbi_points = expected_rbi * scoring_settings['batting'].get('RBI', 0)
        
        batting_points = (
            singles_points + doubles_points + triples_points + hr_points +
            walks_points + runs_points + strikeouts_points + rbi_points
        )
        
        logger.info(f"\n💰 FANTASY POINTS CALCULATION:")
        logger.info(f"   Scoring Settings: {scoring_settings['batting']}")
        logger.info(f"   Singles: {expected_singles:.6f} * {scoring_settings['batting'].get('S', 0)} = {singles_points:.6f}")
        logger.info(f"   Doubles: {expected_doubles:.6f} * {scoring_settings['batting'].get('D', 0)} = {doubles_points:.6f}")
        logger.info(f"   Triples: {expected_triples:.6f} * {scoring_settings['batting'].get('T', 0)} = {triples_points:.6f}")
        logger.info(f"   Home Runs: {expected_home_runs:.6f} * {scoring_settings['batting'].get('HR', 0)} = {hr_points:.6f}")
        logger.info(f"   Walks: {expected_walks:.6f} * {scoring_settings['batting'].get('BB', 0)} = {walks_points:.6f}")
        logger.info(f"   Runs: {expected_runs:.6f} * {scoring_settings['batting'].get('R', 0)} = {runs_points:.6f}")
        logger.info(f"   Strikeouts: {expected_strikeouts:.6f} * {scoring_settings['batting'].get('SO', 0)} = {strikeouts_points:.6f}")
        logger.info(f"   RBI: {expected_rbi:.6f} * {scoring_settings['batting'].get('RBI', 0)} = {rbi_points:.6f}")
        logger.info(f"   TOTAL BATTING POINTS: {batting_points:.6f}")
        logger.info(f"{'='*60}\n")
        
        return {
            'team_abbreviation': team_abbreviation,
            'handedness': handedness,
            'inning': inning,
            'expected_fantasy_points': round(batting_points, 2),
            'expected_runs': round(expected_runs, 3),
            'expected_hits': round(expected_hits, 3),
            'expected_singles': round(expected_singles, 3),
            'expected_doubles': round(expected_doubles, 3),
            'expected_triples': round(expected_triples, 3),
            'expected_home_runs': round(expected_home_runs, 3),
            'expected_walks': round(expected_walks, 3),
            'expected_strikeouts': round(expected_strikeouts, 3),
            'expected_rbi': round(expected_rbi, 3),
            'team_stats': {
                'era': era,
                'whip': whip,
                'k_per_9': k_per_9,
                'bb_per_9': bb_per_9,
                'hr_per_9': hr_per_9,
                'hits_per_9': hits_per_9
            }
        }
    
    @staticmethod
    def calculate_all_teams_expected_points(
        handedness: str,
        inning: int,
        league_type: str,
        custom_scoring: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Calculate expected points for all teams.
        
        Args:
            handedness: Batter handedness ('Lefty' or 'Righty')
            inning: Number of innings to calculate for (1-9)
            league_type: Type of league ('Custom', 'ESPN', 'CBS', 'Yahoo')
            custom_scoring: Custom scoring settings (if league_type is 'Custom')
            
        Returns:
            List of dictionaries containing expected points for all teams
        """
        logger.info(f"\n🏟️ CALCULATING ALL TEAMS EXPECTED POINTS")
        logger.info(f"Parameters: {handedness} batters, {inning} innings, {league_type} league")
        
        # Get scoring settings
        if league_type.upper() == 'CUSTOM' and custom_scoring:
            scoring_settings = custom_scoring
            logger.info(f"Using custom scoring settings: {custom_scoring}")
        else:
            scoring_settings = FantasyCalculatorService.get_scoring_settings(league_type)
            logger.info(f"Using {league_type} scoring settings: {scoring_settings}")
        
        # Get all teams
        teams = Team.query.all()
        results = []
        
        logger.info(f"Processing {len(teams)} teams...")
        
        for team in teams:
            try:
                result = FantasyCalculatorService.calculate_expected_points(
                    team.abbreviation,
                    handedness,
                    inning,
                    scoring_settings
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error calculating for team {team.abbreviation}: {e}")
                continue
        
        # Sort by expected fantasy points (descending)
        results.sort(key=lambda x: x['expected_fantasy_points'], reverse=True)
        
        # Log summary
        if results:
            logger.info(f"\n📊 CALCULATION SUMMARY:")
            logger.info(f"   Total teams processed: {len(results)}")
            logger.info(f"   Highest expected points: {results[0]['team_abbreviation']} ({results[0]['expected_fantasy_points']:.3f})")
            logger.info(f"   Lowest expected points: {results[-1]['team_abbreviation']} ({results[-1]['expected_fantasy_points']:.3f})")
            avg_points = sum(r['expected_fantasy_points'] for r in results) / len(results)
            logger.info(f"   Average expected points: {avg_points:.3f}")
            logger.info(f"🏟️ ALL TEAMS CALCULATION COMPLETE\n")
        
        return results
    
    @staticmethod
    def save_expected_game(
        team_abbreviation: str,
        handedness: str,
        inning: int,
        league_type: str,
        scoring_settings: Dict,
        expected_stats: Dict
    ) -> ExpectedGame:
        """
        Save expected game calculation to database.
        
        Args:
            team_abbreviation: Team abbreviation
            handedness: Batter handedness
            inning: Number of innings
            league_type: League type
            scoring_settings: Scoring settings used
            expected_stats: Calculated expected statistics
            
        Returns:
            ExpectedGame instance
        """
        expected_game = ExpectedGame(
            team_abbreviation=team_abbreviation,
            handedness=handedness,
            inning=inning,
            league_type=league_type,
            scoring_settings=scoring_settings,
            expected_fantasy_points=expected_stats.get('expected_fantasy_points', 0),
            expected_runs=expected_stats.get('expected_runs', 0),
            expected_hits=expected_stats.get('expected_hits', 0),
            expected_home_runs=expected_stats.get('expected_home_runs', 0),
            expected_strikeouts=expected_stats.get('expected_strikeouts', 0),
            expected_walks=expected_stats.get('expected_walks', 0)
        )
        
        db.session.add(expected_game)
        db.session.commit()
        
        return expected_game


class TeamService:
    """Service for team-related operations."""
    
    @staticmethod
    def get_all_teams() -> List[Dict]:
        """
        Get all teams with their statistics.
        
        Returns:
            List of team dictionaries
        """
        teams = Team.query.all()
        return [team.to_dict() for team in teams]
    
    @staticmethod
    def get_team_by_abbreviation(abbreviation: str) -> Optional[Dict]:
        """
        Get a specific team by abbreviation.
        
        Args:
            abbreviation: Team abbreviation
            
        Returns:
            Team dictionary or None if not found
        """
        team = Team.query.filter_by(abbreviation=abbreviation).first()
        return team.to_dict() if team else None
    
    @staticmethod
    def update_team_stats(abbreviation: str, stats: Dict) -> Optional[Dict]:
        """
        Update team statistics.
        
        Args:
            abbreviation: Team abbreviation
            stats: Dictionary of stats to update
            
        Returns:
            Updated team dictionary or None if not found
        """
        team = Team.query.filter_by(abbreviation=abbreviation).first()
        if not team:
            return None
        
        # Update allowed fields
        allowed_fields = [
            'vs_lefty_era', 'vs_lefty_whip', 'vs_lefty_k_per_9',
            'vs_lefty_bb_per_9', 'vs_lefty_hr_per_9', 'vs_lefty_hits_per_9',
            'vs_righty_era', 'vs_righty_whip', 'vs_righty_k_per_9',
            'vs_righty_bb_per_9', 'vs_righty_hr_per_9', 'vs_righty_hits_per_9'
        ]
        
        for field, value in stats.items():
            if field in allowed_fields and hasattr(team, field):
                setattr(team, field, value)
        
        db.session.commit()
        return team.to_dict()
