#!/usr/bin/env python3
"""
Script to run MLB Team Statistics API BDD tests
Tests the actual MLBStatsExtractor service from the application
"""
import os
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run the BDD tests with various output formats"""
    
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "junit").mkdir(exist_ok=True)
    
    print("🚀 Running MLB Team Statistics API BDD Tests...")
    print("📋 Testing actual MLBStatsExtractor service from the application")
    print("=" * 70)
    
    # Run tests with pretty output
    try:
        result = subprocess.run([
            "behave", 
            "-v",
            "--format=pretty",
            "--junit",
            "--junit-directory=reports/junit"
        ], check=True, capture_output=False)
        
        print("\n" + "=" * 70)
        print("✅ All tests passed successfully!")
        print("🎯 The MLBStatsExtractor service is working correctly!")
        
        # Check if JUnit reports were generated
        junit_files = list((reports_dir / "junit").glob("*.xml"))
        if junit_files:
            print(f"📊 JUnit reports generated: {len(junit_files)} files")
            for junit_file in junit_files:
                print(f"   - {junit_file}")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code: {e.returncode}")
        print("🔍 Check the output above for details on which tests failed")
        return e.returncode
    
    except FileNotFoundError:
        print("❌ Error: 'behave' command not found. Please install requirements:")
        print("   pip install -r requirements.txt")
        return 1

def main():
    """Main entry point"""
    return run_tests()

if __name__ == "__main__":
    sys.exit(main())
