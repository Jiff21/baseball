"""
BDD-style tests for calculation service using example statistics.
These tests validate all calculation logic with realistic baseball data.
"""
import pytest
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.calculation_service import CalculationService
from models_new import ScoringSettings


class TestCalculationServiceBDD:
    """BDD tests for the calculation service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc_service = CalculationService()
        
        # Example hitting stats for Los Angeles Dodgers vs Lefty Pitchers (realistic 2024 data)
        self.dodgers_vs_lefty = {
            'team_abbreviation': 'LAD',
            'team_name': 'Los Angeles Dodgers',
            'split_type': 'lefty',
            'season': 2024,
            'games': 138,
            'plate_appearances': 1741,
            'at_bats': 1523,
            'runs': 267,
            'hits': 417,
            'singles': 263,  # calculated: hits - doubles - triples - home_runs
            'doubles': 88,
            'triples': 0,
            'home_runs': 66,
            'rbis': 254,
            'walks': 151,
            'intentional_walks': 12,
            'hit_by_pitch': 26,
            'strikeouts': 345,
            'stolen_bases': 47,
            'caught_stealing': 8,
            'total_bases': 711,
            'wins': 17,
            'losses': 26
        }
        
        # Example hitting stats for Boston Red Sox vs Righty Pitchers
        self.red_sox_vs_righty = {
            'team_abbreviation': 'BOS',
            'team_name': 'Boston Red Sox',
            'split_type': 'righty',
            'season': 2024,
            'games': 119,
            'plate_appearances': 4234,
            'at_bats': 3721,
            'runs': 612,
            'hits': 1089,
            'singles': 721,
            'doubles': 234,
            'triples': 18,
            'home_runs': 116,
            'rbis': 583,
            'walks': 398,
            'intentional_walks': 23,
            'hit_by_pitch': 67,
            'strikeouts': 892,
            'stolen_bases': 78,
            'caught_stealing': 19,
            'total_bases': 1707,
            'wins': 64,
            'losses': 55
        }
    
    def test_given_dodgers_vs_lefty_stats_when_calculating_per_pa_rates_then_returns_correct_rates(self):
        """
        Given: Dodgers vs lefty hitting statistics
        When: Calculating per-plate-appearance rates
        Then: Returns mathematically correct rates
        """
        # When
        rates = self.calc_service.calculate_per_pa_rates(self.dodgers_vs_lefty)
        
        # Then
        assert rates['team_abbreviation'] == 'LAD'
        assert rates['split_type'] == 'lefty'
        assert rates['season'] == 2024
        
        # Validate key per-PA rates (using realistic tolerances)
        expected_hr_per_pa = 66 / 1741  # 0.0379
        assert abs(rates['home_runs_per_pa'] - expected_hr_per_pa) < 0.0001
        
        expected_walks_per_pa = 151 / 1741  # 0.0867
        assert abs(rates['walks_per_pa'] - expected_walks_per_pa) < 0.0001
        
        expected_strikeouts_per_pa = 345 / 1741  # 0.1982
        assert abs(rates['strikeouts_per_pa'] - expected_strikeouts_per_pa) < 0.0001
        
        expected_total_bases_per_pa = 711 / 1741  # 0.4084
        assert abs(rates['total_bases_per_pa'] - expected_total_bases_per_pa) < 0.0001
        
        # Validate PA per inning calculation: (PA/Games)/9
        expected_pa_per_inning = (1741 / 138) / 9  # 1.402
        assert abs(rates['pa_per_inning'] - expected_pa_per_inning) < 0.001
        
        # Validate wins/losses per game
        expected_wins_per_game = 17 / 138  # 0.123
        expected_losses_per_game = 26 / 138  # 0.188
        assert abs(rates['wins_per_game'] - expected_wins_per_game) < 0.001
        assert abs(rates['losses_per_game'] - expected_losses_per_game) < 0.001
    
    def test_given_red_sox_vs_righty_stats_when_calculating_per_pa_rates_then_returns_correct_rates(self):
        """
        Given: Red Sox vs righty hitting statistics
        When: Calculating per-plate-appearance rates
        Then: Returns mathematically correct rates
        """
        # When
        rates = self.calc_service.calculate_per_pa_rates(self.red_sox_vs_righty)
        
        # Then
        assert rates['team_abbreviation'] == 'BOS'
        assert rates['split_type'] == 'righty'
        
        # Validate key rates
        expected_hr_per_pa = 116 / 4234  # 0.0274
        assert abs(rates['home_runs_per_pa'] - expected_hr_per_pa) < 0.0001
        
        expected_runs_per_pa = 612 / 4234  # 0.1446
        assert abs(rates['runs_per_pa'] - expected_runs_per_pa) < 0.0001
        
        expected_pa_per_inning = (4234 / 119) / 9  # 3.956
        assert abs(rates['pa_per_inning'] - expected_pa_per_inning) < 0.001
    
    def test_given_calculated_rates_when_calculating_expected_stats_for_6_innings_then_returns_correct_projections(self):
        """
        Given: Calculated per-PA rates for Dodgers vs lefty
        When: Calculating expected stats for 6 innings
        Then: Returns mathematically correct projections
        """
        # Given
        rates = self.calc_service.calculate_per_pa_rates(self.dodgers_vs_lefty)
        starter_innings = 6.0
        
        # When
        expected = self.calc_service.calculate_expected_stats(rates, starter_innings)
        
        # Then
        expected_pa = rates['pa_per_inning'] * starter_innings  # 1.402 * 6 = 8.412
        assert abs(expected['expected_plate_appearances'] - expected_pa) < 0.001
        
        # Validate expected statistics
        expected_hr = expected_pa * rates['home_runs_per_pa']  # 8.412 * 0.0379 = 0.319
        assert abs(expected['expected_home_runs'] - expected_hr) < 0.001
        
        expected_walks = expected_pa * rates['walks_per_pa']  # 8.412 * 0.0867 = 0.729
        assert abs(expected['expected_walks'] - expected_walks) < 0.001
        
        expected_strikeouts = expected_pa * rates['strikeouts_per_pa']  # 8.412 * 0.1982 = 1.668
        assert abs(expected['expected_strikeouts'] - expected_strikeouts) < 0.001
        
        # Validate expected hits calculation (singles + doubles + triples + home runs)
        expected_singles = expected_pa * rates['singles_per_pa']
        expected_doubles = expected_pa * rates['doubles_per_pa']
        expected_triples = expected_pa * rates['triples_per_pa']
        expected_hits_calc = expected_singles + expected_doubles + expected_triples + expected_hr
        assert abs(expected['expected_hits'] - expected_hits_calc) < 0.001
    
    def test_given_expected_stats_when_calculating_fantasy_points_with_default_scoring_then_returns_correct_points(self):
        """
        Given: Expected statistics for a team
        When: Calculating fantasy points with default scoring settings
        Then: Returns mathematically correct fantasy points
        """
        # Given
        rates = self.calc_service.calculate_per_pa_rates(self.dodgers_vs_lefty)
        expected = self.calc_service.calculate_expected_stats(rates, 6.0)
        
        # When (fantasy points are calculated automatically in calculate_expected_stats)
        fantasy_points = expected['expected_fantasy_points']
        
        # Then - manually calculate expected fantasy points to validate
        scoring = ScoringSettings.get_default_settings()['batting']
        
        manual_calculation = (
            expected['expected_singles'] * scoring['S'] +
            expected['expected_doubles'] * scoring['D'] +
            expected['expected_triples'] * scoring['T'] +
            expected['expected_home_runs'] * scoring['HR'] +
            expected['expected_walks'] * scoring['BB'] +
            expected['expected_ibb'] * scoring['IBB'] +
            expected['expected_hbp'] * scoring['HBP'] +
            expected['expected_runs'] * scoring['R'] +
            expected['expected_rbis'] * scoring['RBI'] +
            expected['expected_stolen_bases'] * scoring['SB'] +
            expected['expected_caught_stealing'] * scoring['CS'] +
            expected['expected_strikeouts'] * scoring['SO'] +
            expected['expected_total_bases'] * scoring['TB']
        )
        
        assert abs(fantasy_points - manual_calculation) < 0.01
    
    def test_given_different_starter_innings_when_calculating_expected_stats_then_scales_proportionally(self):
        """
        Given: Same team rates but different starter innings
        When: Calculating expected stats
        Then: Results scale proportionally with innings
        """
        # Given
        rates = self.calc_service.calculate_per_pa_rates(self.dodgers_vs_lefty)
        
        # When
        expected_6_innings = self.calc_service.calculate_expected_stats(rates, 6.0)
        expected_3_innings = self.calc_service.calculate_expected_stats(rates, 3.0)
        
        # Then - 3 innings should be exactly half of 6 innings
        assert abs(expected_3_innings['expected_plate_appearances'] - 
                  expected_6_innings['expected_plate_appearances'] / 2) < 0.001
        
        assert abs(expected_3_innings['expected_home_runs'] - 
                  expected_6_innings['expected_home_runs'] / 2) < 0.001
        
        assert abs(expected_3_innings['expected_fantasy_points'] - 
                  expected_6_innings['expected_fantasy_points'] / 2) < 0.01
    
    def test_given_zero_plate_appearances_when_calculating_rates_then_returns_zero_rates(self):
        """
        Given: Team stats with zero plate appearances
        When: Calculating per-PA rates
        Then: Returns all zero rates without errors
        """
        # Given
        zero_pa_stats = self.dodgers_vs_lefty.copy()
        zero_pa_stats['plate_appearances'] = 0
        zero_pa_stats['games'] = 0
        
        # When
        rates = self.calc_service.calculate_per_pa_rates(zero_pa_stats)
        
        # Then
        assert rates['home_runs_per_pa'] == 0.0
        assert rates['walks_per_pa'] == 0.0
        assert rates['pa_per_inning'] == 0.0
        assert rates['wins_per_game'] == 0.0
    
    def test_given_invalid_hitting_stats_when_validating_then_returns_appropriate_errors(self):
        """
        Given: Invalid hitting statistics
        When: Validating the data
        Then: Returns appropriate error messages
        """
        # Given - stats with inconsistent hits breakdown
        invalid_stats = self.dodgers_vs_lefty.copy()
        invalid_stats['hits'] = 500  # But singles+doubles+triples+HR = 417
        
        # When
        is_valid, errors = self.calc_service.validate_hitting_stats(invalid_stats)
        
        # Then
        assert not is_valid
        assert any('Hits' in error and 'doesn\'t match' in error for error in errors)
    
    def test_given_realistic_team_stats_when_calculating_full_workflow_then_produces_reasonable_results(self):
        """
        Given: Realistic team hitting statistics
        When: Running the complete calculation workflow
        Then: Produces reasonable fantasy baseball results
        """
        # Given
        team_stats = self.red_sox_vs_righty
        
        # When - full workflow
        rates = self.calc_service.calculate_per_pa_rates(team_stats)
        expected_6_innings = self.calc_service.calculate_expected_stats(rates, 6.0)
        expected_9_innings = self.calc_service.calculate_expected_stats(rates, 9.0)
        
        # Then - validate reasonable ranges for 6 innings
        assert 5.0 <= expected_6_innings['expected_plate_appearances'] <= 30.0
        assert 0.0 <= expected_6_innings['expected_home_runs'] <= 2.0
        assert 0.0 <= expected_6_innings['expected_walks'] <= 5.0
        assert 0.0 <= expected_6_innings['expected_strikeouts'] <= 8.0
        assert -5.0 <= expected_6_innings['expected_fantasy_points'] <= 20.0
        
        # Validate that 9 innings produces higher numbers than 6 innings
        assert expected_9_innings['expected_plate_appearances'] > expected_6_innings['expected_plate_appearances']
        assert expected_9_innings['expected_home_runs'] > expected_6_innings['expected_home_runs']
        assert expected_9_innings['expected_fantasy_points'] > expected_6_innings['expected_fantasy_points']
    
    def test_given_espn_scoring_settings_when_calculating_fantasy_points_then_uses_correct_multipliers(self):
        """
        Given: Expected statistics and ESPN scoring settings
        When: Calculating fantasy points
        Then: Uses ESPN-specific scoring multipliers
        """
        # Given
        rates = self.calc_service.calculate_per_pa_rates(self.dodgers_vs_lefty)
        espn_scoring = ScoringSettings.get_espn_settings()
        
        # When
        expected = self.calc_service.calculate_expected_stats(rates, 6.0, espn_scoring)
        
        # Then - should be different from default scoring
        default_expected = self.calc_service.calculate_expected_stats(rates, 6.0)
        assert expected['expected_fantasy_points'] != default_expected['expected_fantasy_points']
        
        # Validate that strikeouts have the ESPN penalty (-0.5 instead of -1.0)
        espn_so_penalty = expected['expected_strikeouts'] * espn_scoring['batting']['SO']
        default_so_penalty = expected['expected_strikeouts'] * -1.0
        assert espn_so_penalty > default_so_penalty  # ESPN penalty is less severe
    
    def test_given_calculation_summary_when_generating_debug_info_then_returns_useful_summary(self):
        """
        Given: Expected statistics calculation
        When: Generating calculation summary for debugging
        Then: Returns useful summary information
        """
        # Given
        rates = self.calc_service.calculate_per_pa_rates(self.dodgers_vs_lefty)
        expected = self.calc_service.calculate_expected_stats(rates, 6.0)
        
        # When
        summary = self.calc_service.get_calculation_summary(expected)
        
        # Then
        assert summary['team'] == 'LAD'
        assert summary['handedness'] == 'lefty'
        assert summary['starter_innings'] == 6.0
        assert summary['expected_pa'] > 0
        assert 'key_stats' in summary
        assert 'runs' in summary['key_stats']
        assert 'home_runs' in summary['key_stats']


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v'])
