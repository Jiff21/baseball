#!/usr/bin/env python3
"""
Test script to demonstrate the comprehensive logging functionality.
This script shows both single team and all teams calculations with detailed debug output.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services import FantasyCalculatorService

def test_single_team_calculation():
    """Test calculation for a single team with detailed logging."""
    print("\n" + "="*80)
    print("🧪 TESTING SINGLE TEAM CALCULATION")
    print("="*80)
    
    try:
        # Test with Houston Astros vs Lefties for 6 innings
        result = FantasyCalculatorService.calculate_expected_points(
            team_abbreviation='HOU',
            handedness='Lefty',
            inning=6,
            scoring_settings={
                'batting': {
                    'S': 1,    # Singles
                    'D': 2,    # Doubles  
                    'T': 3,    # Triples
                    'HR': 4,   # Home Runs
                    'BB': 1,   # Walks
                    'R': 1,    # Runs
                    'RBI': 1,  # RBI
                    'SO': -1   # Strikeouts
                }
            }
        )
        
        print(f"\n✅ SINGLE TEAM RESULT:")
        print(f"   Team: {result['team_abbreviation']}")
        print(f"   Expected Fantasy Points: {result['expected_fantasy_points']}")
        print(f"   Expected Hits: {result['expected_hits']}")
        print(f"   Expected Home Runs: {result['expected_home_runs']}")
        print(f"   Expected Runs: {result['expected_runs']}")
        
    except Exception as e:
        print(f"❌ Error in single team calculation: {e}")

def test_all_teams_calculation():
    """Test calculation for all teams with summary logging."""
    print("\n" + "="*80)
    print("🧪 TESTING ALL TEAMS CALCULATION")
    print("="*80)
    
    try:
        # Test with all teams vs Righties for 7 innings using ESPN scoring
        results = FantasyCalculatorService.calculate_all_teams_expected_points(
            handedness='Righty',
            inning=7,
            league_type='ESPN'
        )
        
        print(f"\n✅ ALL TEAMS RESULTS:")
        print(f"   Total teams calculated: {len(results)}")
        if results:
            print(f"   Top 3 teams:")
            for i, result in enumerate(results[:3]):
                print(f"     {i+1}. {result['team_abbreviation']}: {result['expected_fantasy_points']} pts")
        
    except Exception as e:
        print(f"❌ Error in all teams calculation: {e}")

def main():
    """Main function to run the debug tests."""
    print("🐍 FANTASY BASEBALL DEBUG LOGGING TEST")
    print("This script demonstrates the comprehensive logging added to the backend.")
    print("Watch the console output for detailed calculation breakdowns!")
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Test single team calculation
        test_single_team_calculation()
        
        # Test all teams calculation  
        test_all_teams_calculation()
    
    print("\n" + "="*80)
    print("🎉 DEBUG LOGGING TEST COMPLETED!")
    print("="*80)
    print("\nThe detailed logging output above shows:")
    print("📊 Raw team statistics from the database")
    print("🧮 Step-by-step per_9 calculations")
    print("⚾ Hit distribution breakdowns")
    print("💰 Fantasy points calculations with individual contributions")
    print("📈 Summary statistics for all teams")
    print("\nThis logging will appear whenever you:")
    print("• Make API calls to /api/calculate-expected")
    print("• Make API calls to /api/calculate-team-expected") 
    print("• Use the frontend application (calculations trigger backend logging)")

if __name__ == '__main__':
    main()

