#!/usr/bin/env python3
"""
Development runner script for the Fantasy Baseball application.
Starts both backend and frontend servers concurrently.
"""
import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def run_backend():
    """Run the Flask backend server."""
    backend_dir = Path(__file__).parent / 'backend'
    os.chdir(backend_dir)
    
    print("🐍 Starting Flask backend server...")
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server failed: {e}")

def run_frontend():
    """Run the React frontend server."""
    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)
    
    print("⚛️  Starting React frontend server...")
    try:
        subprocess.run(['npm', 'start'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server failed: {e}")

def check_dependencies():
    """Check if required dependencies are installed."""
    backend_dir = Path(__file__).parent / 'backend'
    frontend_dir = Path(__file__).parent / 'frontend'
    
    # Check Python dependencies
    requirements_file = backend_dir / 'requirements.txt'
    if not requirements_file.exists():
        print("❌ Backend requirements.txt not found")
        return False
    
    # Check Node dependencies
    package_json = frontend_dir / 'package.json'
    node_modules = frontend_dir / 'node_modules'
    if not package_json.exists():
        print("❌ Frontend package.json not found")
        return False
    
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        os.chdir(frontend_dir)
        try:
            subprocess.run(['npm', 'install'], check=True)
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    
    return True

def main():
    """Main function to start both servers."""
    print("🚀 Fantasy Baseball Development Server")
    print("=" * 40)
    
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    print("✅ Dependencies checked")
    print("\n🌐 Servers will be available at:")
    print("   Backend:  http://localhost:8000")
    print("   Frontend: http://localhost:3000")
    print("\n💡 Press Ctrl+C to stop both servers")
    print("=" * 40)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    try:
        # Start frontend in main thread
        run_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        print("✅ Development servers stopped")

if __name__ == '__main__':
    main()

