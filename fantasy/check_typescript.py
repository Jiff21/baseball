#!/usr/bin/env python3
"""
TypeScript compilation checker for Fantasy Baseball app.
This script checks for TypeScript compilation errors before running E2E tests.
"""

import subprocess
import sys
import os
import json

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out: {command}")
        return None

def check_typescript_compilation():
    """Check TypeScript compilation in the frontend."""
    print("🔍 Checking TypeScript compilation...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    if not os.path.exists(frontend_dir):
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return False
    
    # Check if node_modules exists
    node_modules = os.path.join(frontend_dir, 'node_modules')
    if not os.path.exists(node_modules):
        print("📦 Installing npm dependencies...")
        install_result = run_command("npm install", cwd=frontend_dir)
        if install_result and install_result.returncode != 0:
            print(f"❌ npm install failed: {install_result.stderr}")
            return False
    
    # Run TypeScript compilation check
    print("🔧 Running TypeScript compilation check...")
    tsc_result = run_command("npx tsc --noEmit", cwd=frontend_dir)
    
    if tsc_result is None:
        print("❌ TypeScript check timed out")
        return False
    
    if tsc_result.returncode == 0:
        print("✅ TypeScript compilation successful - no errors found!")
        return True
    else:
        print("❌ TypeScript compilation errors found:")
        print(tsc_result.stdout)
        print(tsc_result.stderr)
        return False

def check_build():
    """Check if the app can build successfully."""
    print("🏗️  Checking if app builds successfully...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Try to build the app
    build_result = run_command("npm run build", cwd=frontend_dir)
    
    if build_result is None:
        print("❌ Build check timed out")
        return False
    
    if build_result.returncode == 0:
        print("✅ App builds successfully!")
        return True
    else:
        print("❌ Build failed:")
        print(build_result.stdout)
        print(build_result.stderr)
        return False

def main():
    """Main function to run all checks."""
    print("🚀 Fantasy Baseball TypeScript Checker")
    print("=" * 50)
    
    # Check TypeScript compilation
    typescript_ok = check_typescript_compilation()
    
    if not typescript_ok:
        print("\n❌ TypeScript compilation failed!")
        print("Please fix the TypeScript errors before running E2E tests.")
        sys.exit(1)
    
    # Check build
    build_ok = check_build()
    
    if not build_ok:
        print("\n❌ Build failed!")
        print("Please fix the build errors before running E2E tests.")
        sys.exit(1)
    
    print("\n🎉 All checks passed!")
    print("✅ TypeScript compilation: OK")
    print("✅ Build: OK")
    print("\n🧪 Ready to run E2E tests!")

if __name__ == '__main__':
    main()

