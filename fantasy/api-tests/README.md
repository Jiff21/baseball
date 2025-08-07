# MLB Team Statistics API BDD Tests

This directory contains Behavior-Driven Development (BDD) tests for the MLB Team Statistics API using Python's `behave` framework.

## Overview

These tests validate the extraction of team statistics from MLB standings data, specifically focusing on:
- Wins/losses against right-handed pitching
- Wins/losses against left-handed pitching  
- Total wins/losses (no splits)

## Test Data

The tests use static JSON data from the 2024 MLB season stored in `features/test_data/mlb_standings_2024.json`. This data includes:
- San Francisco Giants (SF): 80-82 record, 61-57 vs righties, 19-25 vs lefties
- New York Yankees (NYY): 94-68 record, 73-45 vs righties, 21-23 vs lefties

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create reports directory:
```bash
mkdir -p reports/junit
```

## Running Tests

### Run all tests:
```bash
behave
```

### Run with verbose output:
```bash
behave -v
```

### Run specific scenarios:
```bash
behave -n "Extract wins against righties"
```

### Run with tags:
```bash
behave --tags=@smoke
```

### Generate JUnit XML reports:
```bash
behave --junit --junit-directory reports/junit
```

## Test Structure

```
api-tests/
├── features/
│   ├── mlb_team_stats.feature          # BDD feature file with scenarios
│   ├── environment.py                  # Test environment setup
│   ├── step_definitions/
│   │   └── mlb_team_stats_steps.py    # Step implementations
│   └── test_data/
│       └── mlb_standings_2024.json    # Static test data
├── reports/                            # Test reports directory
├── behave.ini                          # Behave configuration
├── requirements.txt                    # Python dependencies
└── README.md                          # This file
```

## Key Components

### MLBStatsExtractor Class
Located in `step_definitions/mlb_team_stats_steps.py`, this helper class provides methods to:
- Find team records by abbreviation
- Extract wins/losses against righties (`record_right` field)
- Extract wins/losses against lefties (`record_left` field)  
- Extract total wins/losses (`wins`/`losses` fields)

### Step Definitions
The step definitions map Gherkin language to Python code:
- `Given I load the json from the mock api call` - Loads static JSON data
- `When I am getting expected wins against Righties for "SF"` - Extracts specific stats
- `Then the expected wins against Righties will be 61 for "SF"` - Validates results

## Example Test Scenarios

```gherkin
Scenario Outline: Extract wins against righties for teams
  When I am getting expected wins against Righties for "<team>"
  Then the expected wins against Righties will be <wins> for "<team>"

  Examples:
    | team | wins |
    | SF   | 61   |
    | NYY  | 73   |
```

## Integration with Fantasy Baseball API

These tests validate the data extraction logic that would be used in the fantasy baseball application to:
1. Parse MLB standings data from external APIs
2. Extract team performance splits (vs lefties/righties)
3. Calculate expected wins/losses for fantasy projections
4. Provide accurate team statistics for fantasy calculations

## Extending Tests

To add new test scenarios:
1. Add new scenarios to `mlb_team_stats.feature`
2. Implement corresponding step definitions in `mlb_team_stats_steps.py`
3. Add new test data to `mlb_standings_2024.json` if needed
4. Update the `MLBStatsExtractor` class with new extraction methods
