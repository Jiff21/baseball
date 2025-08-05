"""
Calculation Service for computing per-plate-appearance rates and expected statistics.
This service handles all the mathematical calculations for the fantasy baseball system.
"""
import logging
from typing import Dict, List, Optional, Tuple
from models_new import ScoringSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CalculationService:
    """Service for calculating per-PA rates and expected statistics."""
    
    def __init__(self):
        self.scoring_settings = ScoringSettings()
    
    def calculate_per_pa_rates(self, hitting_stats: Dict) -> Dict:
        """
        Calculate per-plate-appearance rates from raw hitting statistics.
        
        Args:
            hitting_stats: Raw hitting statistics dictionary
            
        Returns:
            Dictionary with calculated per-PA rates
        """
        plate_appearances = hitting_stats.get('plate_appearances', 0)
        games = hitting_stats.get('games', 0)
        
        if plate_appearances == 0:
            logger.warning(f"Zero plate appearances for team {hitting_stats.get('team_abbreviation', 'Unknown')}")
            return self._get_zero_rates(hitting_stats)
        
        # Calculate per-PA rates
        rates = {
            'team_abbreviation': hitting_stats.get('team_abbreviation', ''),
            'split_type': hitting_stats.get('split_type', ''),
            'season': hitting_stats.get('season', 2024),
            
            # Per-plate-appearance rates (relevant for pitcher performance)
            'strikeouts_per_pa': hitting_stats.get('strikeouts', 0) / plate_appearances,  # K (good for pitcher)
            'runs_per_pa': hitting_stats.get('runs', 0) / plate_appearances,  # Earned Runs (bad for pitcher)
            'walks_per_pa': hitting_stats.get('walks', 0) / plate_appearances,  # Walks Issued (bad for pitcher)
            'singles_per_pa': hitting_stats.get('singles', 0) / plate_appearances,  # Singles Allowed
            'doubles_per_pa': hitting_stats.get('doubles', 0) / plate_appearances,  # Doubles Allowed
            'triples_per_pa': hitting_stats.get('triples', 0) / plate_appearances,  # Triples Allowed
            'home_runs_per_pa': hitting_stats.get('home_runs', 0) / plate_appearances,  # HR Allowed (bad for pitcher)
            'total_bases_per_pa': hitting_stats.get('total_bases', 0) / plate_appearances,  # Total Bases Allowed
            'ibb_per_pa': hitting_stats.get('intentional_walks', 0) / plate_appearances,  # IBB Issued
            'hbp_per_pa': hitting_stats.get('hit_by_pitch', 0) / plate_appearances,  # Hit Batters (bad for pitcher)
            
            # Note: RBI, stolen bases, caught stealing removed - not relevant for pitcher performance
        }
        
        # Calculate plate appearances per inning: (PA/Games)/9
        if games > 0:
            rates['pa_per_inning'] = (plate_appearances / games) / 9
            rates['wins_per_game'] = hitting_stats.get('wins', 0) / games
            rates['losses_per_game'] = hitting_stats.get('losses', 0) / games
        else:
            rates['pa_per_inning'] = 0.0
            rates['wins_per_game'] = 0.0
            rates['losses_per_game'] = 0.0
        
        logger.debug(f"Calculated per-PA rates for {rates['team_abbreviation']} {rates['split_type']}")
        return rates
    
    def _get_zero_rates(self, hitting_stats: Dict) -> Dict:
        """
        Return zero rates when plate appearances is zero.
        
        Args:
            hitting_stats: Raw hitting statistics dictionary
            
        Returns:
            Dictionary with all rates set to zero
        """
        return {
            'team_abbreviation': hitting_stats.get('team_abbreviation', ''),
            'split_type': hitting_stats.get('split_type', ''),
            'season': hitting_stats.get('season', 2024),
            'strikeouts_per_pa': 0.0,  # K (good for pitcher)
            'runs_per_pa': 0.0,  # Earned Runs (bad for pitcher)
            'walks_per_pa': 0.0,  # Walks Issued (bad for pitcher)
            'singles_per_pa': 0.0,  # Singles Allowed
            'doubles_per_pa': 0.0,  # Doubles Allowed
            'triples_per_pa': 0.0,  # Triples Allowed
            'home_runs_per_pa': 0.0,  # HR Allowed (bad for pitcher)
            'total_bases_per_pa': 0.0,  # Total Bases Allowed
            'ibb_per_pa': 0.0,  # IBB Issued
            'hbp_per_pa': 0.0,  # Hit Batters (bad for pitcher)
            'pa_per_inning': 0.0,
            'wins_per_game': 0.0,
            'losses_per_game': 0.0,
            # Note: RBI, stolen bases, caught stealing removed - not relevant for pitcher performance
        }
    
    def calculate_expected_stats(self, 
                               calculated_rates: Dict, 
                               starter_expected_innings: float,
                               scoring_settings: Optional[Dict] = None) -> Dict:
        """
        Calculate expected statistics based on starter innings and per-PA rates.
        
        Args:
            calculated_rates: Per-PA rates dictionary
            starter_expected_innings: Expected innings for the starter
            scoring_settings: Custom scoring settings (optional)
            
        Returns:
            Dictionary with expected statistics and fantasy points
        """
        if scoring_settings is None:
            scoring_settings = self.scoring_settings.get_default_settings()
        
        # Calculate expected plate appearances
        pa_per_inning = calculated_rates.get('pa_per_inning', 0.0)
        expected_pa = starter_expected_innings * pa_per_inning
        
        if expected_pa == 0:
            logger.warning(f"Zero expected PA for team {calculated_rates.get('team_abbreviation', 'Unknown')}")
            return self._get_zero_expected_stats(calculated_rates, starter_expected_innings, scoring_settings)
        
        # Calculate expected statistics (what the pitcher will give up)
        expected_stats = {
            'team_abbreviation': calculated_rates.get('team_abbreviation', ''),
            'handedness': calculated_rates.get('split_type', ''),
            'starter_expected_innings': starter_expected_innings,
            'season': calculated_rates.get('season', 2024),
            'expected_plate_appearances': expected_pa,
            
            # Expected pitcher statistics (what pitcher gives up to this team's offense)
            'expected_runs': expected_pa * calculated_rates.get('runs_per_pa', 0),  # Earned Runs
            'expected_singles': expected_pa * calculated_rates.get('singles_per_pa', 0),
            'expected_doubles': expected_pa * calculated_rates.get('doubles_per_pa', 0),
            'expected_triples': expected_pa * calculated_rates.get('triples_per_pa', 0),
            'expected_home_runs': expected_pa * calculated_rates.get('home_runs_per_pa', 0),  # HR Allowed
            'expected_walks': expected_pa * calculated_rates.get('walks_per_pa', 0),  # Walks Issued
            'expected_strikeouts': expected_pa * calculated_rates.get('strikeouts_per_pa', 0),  # Strikeouts (good for pitcher)
            'expected_total_bases': expected_pa * calculated_rates.get('total_bases_per_pa', 0),  # Total Bases Allowed
            'expected_ibb': expected_pa * calculated_rates.get('ibb_per_pa', 0),  # IBB Issued
            'expected_hbp': expected_pa * calculated_rates.get('hbp_per_pa', 0),  # Hit Batters
            
            # Note: RBI, stolen bases, caught stealing removed - not relevant for pitcher performance
        }
        
        logger.info(f"Expected Stats Calculation for {expected_stats['team_abbreviation']} vs {expected_stats['handedness']}:")
        logger.info(f"  Expected PA: {expected_pa:.2f} (Innings: {starter_expected_innings} × PA/Inn: {pa_per_inning:.3f})")
        logger.info(f"  Expected Hits: {expected_stats.get('expected_singles', 0) + expected_stats.get('expected_doubles', 0) + expected_stats.get('expected_triples', 0) + expected_stats.get('expected_home_runs', 0):.2f}")
        logger.info(f"  Expected HR: {expected_stats.get('expected_home_runs', 0):.2f}")
        logger.info(f"  Expected Walks: {expected_stats.get('expected_walks', 0):.2f}")
        logger.info(f"  Expected Runs: {expected_stats.get('expected_runs', 0):.2f}")
        logger.info(f"  Expected K: {expected_stats.get('expected_strikeouts', 0):.2f}")
        
        # Calculate expected hits (singles + doubles + triples + home runs)
        expected_stats['expected_hits'] = (
            expected_stats['expected_singles'] +
            expected_stats['expected_doubles'] +
            expected_stats['expected_triples'] +
            expected_stats['expected_home_runs']
        )
        
        # Calculate expected fantasy points
        expected_stats['expected_fantasy_points'] = self._calculate_fantasy_points(
            expected_stats, scoring_settings
        )
        
        logger.debug(f"Calculated expected stats for {expected_stats['team_abbreviation']} "
                    f"vs {expected_stats['handedness']} ({starter_expected_innings} IP)")
        
        return expected_stats
    
    def _get_zero_expected_stats(self, calculated_rates: Dict, starter_expected_innings: float, scoring_settings: Dict) -> Dict:
        """
        Return zero expected stats when expected PA is zero.
        
        Args:
            calculated_rates: Per-PA rates dictionary
            starter_expected_innings: Expected innings for the starter
            scoring_settings: Scoring settings dictionary
            
        Returns:
            Dictionary with all expected stats set to zero
        """
        return {
            'team_abbreviation': calculated_rates.get('team_abbreviation', ''),
            'handedness': calculated_rates.get('split_type', ''),
            'starter_expected_innings': starter_expected_innings,
            'season': calculated_rates.get('season', 2024),
            'expected_plate_appearances': 0.0,
            'expected_fantasy_points': 0.0,
            'expected_runs': 0.0,
            'expected_hits': 0.0,
            'expected_singles': 0.0,
            'expected_doubles': 0.0,
            'expected_triples': 0.0,
            'expected_home_runs': 0.0,
            'expected_walks': 0.0,
            'expected_strikeouts': 0.0,
            'expected_total_bases': 0.0,
            'expected_rbis': 0.0,
            'expected_stolen_bases': 0.0,
            'expected_caught_stealing': 0.0,
            'expected_ibb': 0.0,
            'expected_hbp': 0.0,
        }
    
    def _calculate_fantasy_points(self, expected_stats: Dict, scoring_settings: Dict) -> float:
        """
        Calculate fantasy points based on expected statistics and scoring settings.
        
        IMPORTANT: We're calculating what a PITCHER will give up based on team hitting stats,
        so we use PITCHING scoring settings (negative points for hits/runs allowed).
        
        Args:
            expected_stats: Expected statistics dictionary
            scoring_settings: Scoring settings dictionary
            
        Returns:
            Expected fantasy points
        """
        pitching_settings = scoring_settings.get('pitching', {})
        
        fantasy_points = 0.0
        
        # Pitching statistics (what the pitcher gives up to this team's offense)
        fantasy_points += expected_stats.get('expected_hits', 0) * pitching_settings.get('HA', 0)  # Hits Allowed
        fantasy_points += expected_stats.get('expected_home_runs', 0) * pitching_settings.get('HRA', 0)  # HR Allowed
        fantasy_points += expected_stats.get('expected_walks', 0) * pitching_settings.get('BB', 0)  # Walks Issued
        fantasy_points += expected_stats.get('expected_ibb', 0) * pitching_settings.get('IBB', 0)  # IBB Issued
        fantasy_points += expected_stats.get('expected_hbp', 0) * pitching_settings.get('HB', 0)  # Hit Batters
        fantasy_points += expected_stats.get('expected_runs', 0) * pitching_settings.get('ER', 0)  # Earned Runs
        fantasy_points += expected_stats.get('expected_strikeouts', 0) * pitching_settings.get('K', 0)  # Strikeouts (positive for pitcher)
        fantasy_points += expected_stats.get('expected_total_bases', 0) * pitching_settings.get('TB', 0)  # Total Bases Allowed
        
        # Add innings pitched (positive points)
        fantasy_points += expected_stats.get('starter_expected_innings', 0) * pitching_settings.get('INN', 0)
        
        logger.info(f"Fantasy Points Calculation for {expected_stats.get('team_abbreviation', 'Unknown')}:")
        logger.info(f"  Expected Hits: {expected_stats.get('expected_hits', 0):.2f} × HA Score: {pitching_settings.get('HA', 0)} = {expected_stats.get('expected_hits', 0) * pitching_settings.get('HA', 0):.2f}")
        logger.info(f"  Expected HR: {expected_stats.get('expected_home_runs', 0):.2f} × HRA Score: {pitching_settings.get('HRA', 0)} = {expected_stats.get('expected_home_runs', 0) * pitching_settings.get('HRA', 0):.2f}")
        logger.info(f"  Expected Walks: {expected_stats.get('expected_walks', 0):.2f} × BB Score: {pitching_settings.get('BB', 0)} = {expected_stats.get('expected_walks', 0) * pitching_settings.get('BB', 0):.2f}")
        logger.info(f"  Expected Runs: {expected_stats.get('expected_runs', 0):.2f} × ER Score: {pitching_settings.get('ER', 0)} = {expected_stats.get('expected_runs', 0) * pitching_settings.get('ER', 0):.2f}")
        logger.info(f"  Expected K: {expected_stats.get('expected_strikeouts', 0):.2f} × K Score: {pitching_settings.get('K', 0)} = {expected_stats.get('expected_strikeouts', 0) * pitching_settings.get('K', 0):.2f}")
        logger.info(f"  Innings: {expected_stats.get('starter_expected_innings', 0):.1f} × INN Score: {pitching_settings.get('INN', 0)} = {expected_stats.get('starter_expected_innings', 0) * pitching_settings.get('INN', 0):.2f}")
        logger.info(f"  TOTAL FANTASY POINTS: {fantasy_points:.2f}")
        
        return round(fantasy_points, 2)
    
    def validate_hitting_stats(self, hitting_stats: Dict) -> Tuple[bool, List[str]]:
        """
        Validate hitting statistics for data quality.
        
        Args:
            hitting_stats: Raw hitting statistics dictionary
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        required_fields = [
            'team_abbreviation', 'team_name', 'games', 'plate_appearances',
            'hits', 'singles', 'doubles', 'triples', 'home_runs'
        ]
        
        for field in required_fields:
            if field not in hitting_stats:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        # Check data consistency
        plate_appearances = hitting_stats.get('plate_appearances', 0)
        at_bats = hitting_stats.get('at_bats', 0)
        walks = hitting_stats.get('walks', 0)
        hit_by_pitch = hitting_stats.get('hit_by_pitch', 0)
        
        # PA should be approximately AB + BB + HBP (allowing for some variance due to sacrifices, etc.)
        expected_pa = at_bats + walks + hit_by_pitch
        if plate_appearances > 0 and abs(plate_appearances - expected_pa) > (plate_appearances * 0.1):
            errors.append(f"PA ({plate_appearances}) doesn't match AB+BB+HBP ({expected_pa})")
        
        # Check that hits breakdown makes sense
        hits = hitting_stats.get('hits', 0)
        singles = hitting_stats.get('singles', 0)
        doubles = hitting_stats.get('doubles', 0)
        triples = hitting_stats.get('triples', 0)
        home_runs = hitting_stats.get('home_runs', 0)
        
        calculated_hits = singles + doubles + triples + home_runs
        if hits != calculated_hits:
            errors.append(f"Hits ({hits}) doesn't match singles+doubles+triples+HR ({calculated_hits})")
        
        # Check for negative values
        numeric_fields = [
            'games', 'plate_appearances', 'at_bats', 'runs', 'hits',
            'singles', 'doubles', 'triples', 'home_runs', 'rbis',
            'walks', 'intentional_walks', 'hit_by_pitch', 'strikeouts',
            'stolen_bases', 'caught_stealing', 'total_bases', 'wins', 'losses'
        ]
        
        for field in numeric_fields:
            value = hitting_stats.get(field, 0)
            if value < 0:
                errors.append(f"Negative value for {field}: {value}")
        
        # Check reasonable ranges
        if plate_appearances > 0:
            strikeout_rate = hitting_stats.get('strikeouts', 0) / plate_appearances
            if strikeout_rate > 0.5:  # More than 50% strikeout rate is suspicious
                errors.append(f"Unusually high strikeout rate: {strikeout_rate:.3f}")
            
            walk_rate = walks / plate_appearances
            if walk_rate > 0.25:  # More than 25% walk rate is suspicious
                errors.append(f"Unusually high walk rate: {walk_rate:.3f}")
        
        return len(errors) == 0, errors
    
    def get_calculation_summary(self, expected_stats: Dict) -> Dict:
        """
        Generate a summary of calculations for debugging purposes.
        
        Args:
            expected_stats: Expected statistics dictionary
            
        Returns:
            Summary dictionary with calculation details
        """
        return {
            'team': expected_stats.get('team_abbreviation', ''),
            'handedness': expected_stats.get('handedness', ''),
            'starter_innings': expected_stats.get('starter_expected_innings', 0),
            'expected_pa': expected_stats.get('expected_plate_appearances', 0),
            'expected_fantasy_points': expected_stats.get('expected_fantasy_points', 0),
            'key_stats': {
                'runs': expected_stats.get('expected_runs', 0),
                'hits': expected_stats.get('expected_hits', 0),
                'home_runs': expected_stats.get('expected_home_runs', 0),
                'walks': expected_stats.get('expected_walks', 0),
                'strikeouts': expected_stats.get('expected_strikeouts', 0),
                'total_bases': expected_stats.get('expected_total_bases', 0),
            }
        }
