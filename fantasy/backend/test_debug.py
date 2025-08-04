#!/usr/bin/env python3
"""
Test script to demonstrate the debugging output for fantasy calculations.
Run this to see the detailed logging in action.
"""
import os
import sys
import logging

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services import FantasyCalculatorService

# Configure logging to show all debug output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_debug_output():
    """Test the debugging output for fantasy calculations."""
    print("🚀 Starting Fantasy Baseball Debug Test")
    print("=" * 60)
    
    # Create Flask app context
    app = create_app('development')
    
    with app.app_context():
        try:
            # Test single team calculation
            print("\n🏟️ Testing single team calculation (Houston Astros vs Lefties, 6 innings)...")
            result = FantasyCalculatorService.calculate_expected_points(
                team_abbreviation='HOU',
                handedness='Lefty',
                inning=6,
                scoring_settings=FantasyCalculatorService.get_scoring_settings('ESPN')
            )
            print(f"✅ Single team result: {result['expected_fantasy_points']:.3f} points")
            
            print("\n" + "=" * 60)
            print("🏟️ Testing all teams calculation (Righties vs 9 innings)...")
            
            # Test all teams calculation (limit to first 3 teams for demo)
            results = FantasyCalculatorService.calculate_all_teams_expected_points(
                handedness='Righty',
                inning=9,
                league_type='ESPN'
            )
            
            print(f"✅ All teams calculation complete!")
            print(f"📊 Processed {len(results)} teams")
            if results:
                print(f"🥇 Top team: {results[0]['team_abbreviation']} ({results[0]['expected_fantasy_points']:.3f} points)")
                print(f"🥉 Bottom team: {results[-1]['team_abbreviation']} ({results[-1]['expected_fantasy_points']:.3f} points)")
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎯 Debug test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_debug_output()
