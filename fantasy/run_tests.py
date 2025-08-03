#!/usr/bin/env python3
"""
Test runner script for the Fantasy Baseball application.
Runs both backend and frontend tests.
"""
import os
import sys
import subprocess
from pathlib import Path

def run_backend_tests():
    """Run backend Python tests."""
    backend_dir = Path(__file__).parent / 'backend'
    os.chdir(backend_dir)
    
    print("🐍 Running backend tests...")
    print("=" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'test_app.py', 
            '-v', 
            '--tb=short'
        ], check=False)
        
        if result.returncode == 0:
            print("✅ Backend tests passed!")
            return True
        else:
            print("❌ Backend tests failed!")
            return False
            
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False
    except Exception as e:
        print(f"❌ Error running backend tests: {e}")
        return False

def run_frontend_tests():
    """Run frontend React tests."""
    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)
    
    print("\n⚛️  Running frontend tests...")
    print("=" * 40)
    
    try:
        result = subprocess.run([
            'npm', 'run', 'test:ci'
        ], check=False)
        
        if result.returncode == 0:
            print("✅ Frontend tests passed!")
            return True
        else:
            print("❌ Frontend tests failed!")
            return False
            
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js")
        return False
    except Exception as e:
        print(f"❌ Error running frontend tests: {e}")
        return False

def check_test_dependencies():
    """Check if test dependencies are available."""
    backend_dir = Path(__file__).parent / 'backend'
    frontend_dir = Path(__file__).parent / 'frontend'
    
    # Check if backend test file exists
    if not (backend_dir / 'test_app.py').exists():
        print("❌ Backend test file not found")
        return False
    
    # Check if frontend has node_modules
    if not (frontend_dir / 'node_modules').exists():
        print("❌ Frontend dependencies not installed. Run: npm install")
        return False
    
    return True

def main():
    """Main function to run all tests."""
    print("🧪 Fantasy Baseball Test Suite")
    print("=" * 40)
    
    if not check_test_dependencies():
        print("❌ Test dependency check failed")
        sys.exit(1)
    
    backend_passed = run_backend_tests()
    frontend_passed = run_frontend_tests()
    
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    print(f"   Backend:  {'✅ PASSED' if backend_passed else '❌ FAILED'}")
    print(f"   Frontend: {'✅ PASSED' if frontend_passed else '❌ FAILED'}")
    
    if backend_passed and frontend_passed:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()

