"""
Step definitions for MLB Team Statistics API tests
"""
import json
import os
from behave import given, when, then
from pathlib import Path


class MLBStatsExtractor:
    """Helper class to extract team statistics from MLB standings data"""
    
    def __init__(self, standings_data):
        self.standings_data = standings_data
    
    def find_team_record(self, team_abbreviation):
        """Find team record by abbreviation"""
        for record in self.standings_data.get('records', []):
            for team_record in record.get('teamRecords', []):
                if team_record.get('abbreviation') == team_abbreviation:
                    return team_record
        return None
    
    def get_wins_against_righties(self, team_abbreviation):
        """Extract wins against right-handed pitching"""
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_right field (format: "wins-losses")
            record_right = team_record.get('record_right', '0-0')
            wins = int(record_right.split('-')[0])
            return wins
        return 0
    
    def get_losses_against_righties(self, team_abbreviation):
        """Extract losses against right-handed pitching"""
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_right field (format: "wins-losses")
            record_right = team_record.get('record_right', '0-0')
            losses = int(record_right.split('-')[1])
            return losses
        return 0
    
    def get_wins_against_lefties(self, team_abbreviation):
        """Extract wins against left-handed pitching"""
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_left field (format: "wins-losses")
            record_left = team_record.get('record_left', '0-0')
            wins = int(record_left.split('-')[0])
            return wins
        return 0
    
    def get_losses_against_lefties(self, team_abbreviation):
        """Extract losses against left-handed pitching"""
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            # Parse the record_left field (format: "wins-losses")
            record_left = team_record.get('record_left', '0-0')
            losses = int(record_left.split('-')[1])
            return losses
        return 0
    
    def get_total_wins(self, team_abbreviation):
        """Extract total wins (no splits)"""
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            return team_record.get('wins', 0)
        return 0
    
    def get_total_losses(self, team_abbreviation):
        """Extract total losses (no splits)"""
        team_record = self.find_team_record(team_abbreviation)
        if team_record:
            return team_record.get('losses', 0)
        return 0


@given('I load the json from the mock api call')
def step_load_json_from_mock_api(context):
    """Load the static JSON data from test_data directory"""
    # Get the path to the test data file
    current_dir = Path(__file__).parent.parent
    json_file_path = current_dir / 'test_data' / 'mlb_standings_2024.json'
    
    # Load the JSON data
    with open(json_file_path, 'r') as f:
        context.standings_data = json.load(f)
    
    # Initialize the stats extractor
    context.stats_extractor = MLBStatsExtractor(context.standings_data)


@when('I am getting expected wins against Righties for "{team}"')
def step_get_wins_against_righties(context, team):
    """Extract wins against righties for the specified team"""
    context.extracted_wins = context.stats_extractor.get_wins_against_righties(team)


@then('the expected wins against Righties will be {expected_wins:d} for "{team}"')
def step_verify_wins_against_righties(context, expected_wins, team):
    """Verify the extracted wins against righties match expected value"""
    assert context.extracted_wins == expected_wins, \
        f"Expected {expected_wins} wins against righties for {team}, but got {context.extracted_wins}"


@when('I am getting expected losses against Righties for "{team}"')
def step_get_losses_against_righties(context, team):
    """Extract losses against righties for the specified team"""
    context.extracted_losses = context.stats_extractor.get_losses_against_righties(team)


@then('the expected losses against Righties will be {expected_losses:d} for "{team}"')
def step_verify_losses_against_righties(context, expected_losses, team):
    """Verify the extracted losses against righties match expected value"""
    assert context.extracted_losses == expected_losses, \
        f"Expected {expected_losses} losses against righties for {team}, but got {context.extracted_losses}"


@when('I am getting expected wins against Lefties for "{team}"')
def step_get_wins_against_lefties(context, team):
    """Extract wins against lefties for the specified team"""
    context.extracted_wins = context.stats_extractor.get_wins_against_lefties(team)


@then('the expected wins against Lefties will be {expected_wins:d} for "{team}"')
def step_verify_wins_against_lefties(context, expected_wins, team):
    """Verify the extracted wins against lefties match expected value"""
    assert context.extracted_wins == expected_wins, \
        f"Expected {expected_wins} wins against lefties for {team}, but got {context.extracted_wins}"


@when('I am getting expected losses against Lefties for "{team}"')
def step_get_losses_against_lefties(context, team):
    """Extract losses against lefties for the specified team"""
    context.extracted_losses = context.stats_extractor.get_losses_against_lefties(team)


@then('the expected losses against Lefties will be {expected_losses:d} for "{team}"')
def step_verify_losses_against_lefties(context, expected_losses, team):
    """Verify the extracted losses against lefties match expected value"""
    assert context.extracted_losses == expected_losses, \
        f"Expected {expected_losses} losses against lefties for {team}, but got {context.extracted_losses}"


@when('I am getting expected wins with no splits for "{team}"')
def step_get_total_wins(context, team):
    """Extract total wins (no splits) for the specified team"""
    context.extracted_wins = context.stats_extractor.get_total_wins(team)


@then('the expected wins with no splits will be {expected_wins:d} for "{team}"')
def step_verify_total_wins(context, expected_wins, team):
    """Verify the extracted total wins match expected value"""
    assert context.extracted_wins == expected_wins, \
        f"Expected {expected_wins} total wins for {team}, but got {context.extracted_wins}"


@when('I am getting expected losses with no splits for "{team}"')
def step_get_total_losses(context, team):
    """Extract total losses (no splits) for the specified team"""
    context.extracted_losses = context.stats_extractor.get_total_losses(team)


@then('the expected losses with no splits will be {expected_losses:d} for "{team}"')
def step_verify_total_losses(context, expected_losses, team):
    """Verify the extracted total losses match expected value"""
    assert context.extracted_losses == expected_losses, \
        f"Expected {expected_losses} total losses for {team}, but got {context.extracted_losses}"
