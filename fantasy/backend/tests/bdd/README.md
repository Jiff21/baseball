# MLB Team Statistics API BDD Tests

This directory contains Behavior-Driven Development (BDD) tests for the MLB Team Statistics API using Python's `behave` framework. **These tests validate the actual `MLBStatsExtractor` service from the application.**

## Overview

These tests validate the extraction of team statistics from MLB standings data using the real application service, specifically focusing on:
- Wins/losses against right-handed pitching
- Wins/losses against left-handed pitching  
- Total wins/losses (no splits)

## Key Difference from Typical BDD Tests

**These tests import and test the actual `MLBStatsExtractor` service from `backend/services/mlb_stats_service.py`** rather than creating a separate test-only implementation. This ensures we're testing the real code that will be used in production.

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
python run_tests.py
# OR
behave -v
```

### Run with verbose output:
```bash
behave -v
```

### Run specific scenarios:
```bash
behave -n "Extract wins against righties"
```

### Generate JUnit XML reports:
```bash
behave --junit --junit-directory reports/junit
```

## Test Structure

```
backend/tests/bdd/
├── features/
│   ├── mlb_team_stats.feature          # BDD scenarios in Gherkin
│   ├── environment.py                  # Test environment setup
│   ├── steps/
│   │   └── mlb_team_stats_steps.py    # Step implementations (imports real service)
│   └── test_data/
│       └── mlb_standings_2024.json    # Static test data
├── reports/                            # Test reports directory
├── behave.ini                          # Behave configuration
├── requirements.txt                    # Python dependencies
├── run_tests.py                       # Test runner script
└── README.md                          # This file
```

## Key Components

### Real Service Integration
The step definitions in `steps/mlb_team_stats_steps.py` import the actual `MLBStatsExtractor` from:
```python
from services.mlb_stats_service import MLBStatsExtractor
```

This ensures we're testing the real application code, not a test double.

### MLBStatsExtractor Service Features
The service provides methods to:
- `fetch_standings_data()` - Fetch live data from MLB API
- `load_standings_data(data)` - Load static data (used in tests)
- `find_team_record(abbreviation)` - Find team records by abbreviation
- `get_wins_against_righties(team)` - Extract wins vs right-handed pitching
- `get_losses_against_righties(team)` - Extract losses vs right-handed pitching
- `get_wins_against_lefties(team)` - Extract wins vs left-handed pitching
- `get_losses_against_lefties(team)` - Extract losses vs left-handed pitching
- `get_total_wins(team)` - Extract total wins
- `get_total_losses(team)` - Extract total losses
- `get_team_stats_summary(team)` - Get complete team statistics

### Step Definitions
The step definitions map Gherkin language to Python code that calls the real service:
- `Given I load the json from the mock api call` - Loads static JSON data into the service
- `When I am getting expected wins against Righties for "SF"` - Calls the real service method
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

## Integration with Fantasy Baseball Application

These tests validate the actual service that will be used in the fantasy baseball application to:
1. Parse MLB standings data from external APIs
2. Extract team performance splits (vs lefties/righties)
3. Calculate expected wins/losses for fantasy projections
4. Provide accurate team statistics for fantasy calculations

## Using the Service in the Application

The `MLBStatsExtractor` can be used in your application like this:

```python
from services import MLBStatsExtractor

# Initialize and fetch live data
extractor = MLBStatsExtractor()
standings_data = extractor.fetch_standings_data()

# Get team statistics
sf_stats = extractor.get_team_stats_summary('SF')
print(f"SF Giants: {sf_stats}")

# Get specific statistics
sf_wins_vs_righties = extractor.get_wins_against_righties('SF')
```

## Extending Tests

To add new test scenarios:
1. Add new scenarios to `mlb_team_stats.feature`
2. Implement corresponding step definitions in `mlb_team_stats_steps.py`
3. Add new test data to `mlb_standings_2024.json` if needed
4. Extend the `MLBStatsExtractor` service with new methods if required

The key is that any new functionality should be added to the real service first, then tested through these BDD tests.
