"""
Step definitions for MLB Team Statistics API tests
Tests the actual MLBStatsExtractor service from the application
"""
import json
import sys
import os
from pathlib import Path
from behave import given, when, then

# Add the backend directory to the Python path so we can import from services
# We're in fantasy/backend/tests/bdd/features/steps/, so backend is 4 levels up
backend_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

# Import the actual service from the application
from services.mlb_stats_service import MLBStatsExtractor


@given('I load the json from the mock api call')
def step_load_json_from_mock_api(context):
    """Load the static JSON data from test_data directory and initialize the service"""
    # Get the path to the test data file
    current_dir = Path(__file__).parent.parent
    json_file_path = current_dir / 'test_data' / 'mlb_standings_2024.json'
    
    # Load the JSON data
    with open(json_file_path, 'r') as f:
        standings_data = json.load(f)
    
    # Initialize the actual MLBStatsExtractor service from the application
    context.stats_extractor = MLBStatsExtractor()
    context.stats_extractor.load_standings_data(standings_data)


@when('I am getting expected wins against Righties for "{team}"')
def step_get_wins_against_righties(context, team):
    """Extract wins against righties for the specified team using the actual service"""
    context.extracted_wins = context.stats_extractor.get_wins_against_righties(team)


@then('the expected wins against Righties will be {expected_wins:d} for "{team}"')
def step_verify_wins_against_righties(context, expected_wins, team):
    """Verify the extracted wins against righties match expected value"""
    assert context.extracted_wins == expected_wins, \
        f"Expected {expected_wins} wins against righties for {team}, but got {context.extracted_wins}"


@when('I am getting expected losses against Righties for "{team}"')
def step_get_losses_against_righties(context, team):
    """Extract losses against righties for the specified team using the actual service"""
    context.extracted_losses = context.stats_extractor.get_losses_against_righties(team)


@then('the expected losses against Righties will be {expected_losses:d} for "{team}"')
def step_verify_losses_against_righties(context, expected_losses, team):
    """Verify the extracted losses against righties match expected value"""
    assert context.extracted_losses == expected_losses, \
        f"Expected {expected_losses} losses against righties for {team}, but got {context.extracted_losses}"


@when('I am getting expected wins against Lefties for "{team}"')
def step_get_wins_against_lefties(context, team):
    """Extract wins against lefties for the specified team using the actual service"""
    context.extracted_wins = context.stats_extractor.get_wins_against_lefties(team)


@then('the expected wins against Lefties will be {expected_wins:d} for "{team}"')
def step_verify_wins_against_lefties(context, expected_wins, team):
    """Verify the extracted wins against lefties match expected value"""
    assert context.extracted_wins == expected_wins, \
        f"Expected {expected_wins} wins against lefties for {team}, but got {context.extracted_wins}"


@when('I am getting expected losses against Lefties for "{team}"')
def step_get_losses_against_lefties(context, team):
    """Extract losses against lefties for the specified team using the actual service"""
    context.extracted_losses = context.stats_extractor.get_losses_against_lefties(team)


@then('the expected losses against Lefties will be {expected_losses:d} for "{team}"')
def step_verify_losses_against_lefties(context, expected_losses, team):
    """Verify the extracted losses against lefties match expected value"""
    assert context.extracted_losses == expected_losses, \
        f"Expected {expected_losses} losses against lefties for {team}, but got {context.extracted_losses}"


@when('I am getting expected wins with no splits for "{team}"')
def step_get_total_wins(context, team):
    """Extract total wins (no splits) for the specified team using the actual service"""
    context.extracted_wins = context.stats_extractor.get_total_wins(team)


@then('the expected wins with no splits will be {expected_wins:d} for "{team}"')
def step_verify_total_wins(context, expected_wins, team):
    """Verify the extracted total wins match expected value"""
    assert context.extracted_wins == expected_wins, \
        f"Expected {expected_wins} total wins for {team}, but got {context.extracted_wins}"


@when('I am getting expected losses with no splits for "{team}"')
def step_get_total_losses(context, team):
    """Extract total losses (no splits) for the specified team using the actual service"""
    context.extracted_losses = context.stats_extractor.get_total_losses(team)


@then('the expected losses with no splits will be {expected_losses:d} for "{team}"')
def step_verify_total_losses(context, expected_losses, team):
    """Verify the extracted total losses match expected value"""
    assert context.extracted_losses == expected_losses, \
        f"Expected {expected_losses} total losses for {team}, but got {context.extracted_losses}"
