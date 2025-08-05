#!/usr/bin/env python3
"""
Happy Path Dependency Installer

This script helps install Python dependencies for the Happy Path project,
with special handling for common macOS issues with psycopg2.
"""

import sys
import subprocess
import platform
from pathlib import Path


def check_homebrew():
    """Check if Homebrew is installed (macOS only)."""
    if platform.system() != "Darwin":
        return True
        
    try:
        subprocess.run(["brew", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Homebrew not found. Install from: https://brew.sh/")
        return False


def install_postgresql_dev_tools():
    """Install PostgreSQL development tools."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        if not check_homebrew():
            return False
            
        try:
            print("Installing PostgreSQL development libraries via Homebrew...")
            subprocess.run(
                ["brew", "install", "postgresql@15"], 
                check=True
            )
            print("✓ PostgreSQL development libraries installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PostgreSQL development libraries")
            return False
            
    elif system == "Linux":
        print("On Linux, install PostgreSQL development libraries with:")
        print("  Ubuntu/Debian: sudo apt-get install libpq-dev python3-dev")
        print("  CentOS/RHEL: sudo yum install postgresql-devel python3-devel")
        print("  Fedora: sudo dnf install postgresql-devel python3-devel")
        return False
        
    else:
        print(f"Unsupported system: {system}")
        return False


def install_python_packages():
    """Install Python packages with fallback strategies."""
    strategies = [
        # Strategy 1: Install latest psycopg2-binary
        {
            "name": "Latest psycopg2-binary",
            "commands": [
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                [sys.executable, "-m", "pip", "install", "psycopg2-binary>=2.9.9"],
            ]
        },
        # Strategy 2: Install from requirements-dev.txt
        {
            "name": "Development requirements",
            "commands": [
                [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
            ]
        },
        # Strategy 3: Install minimal dependencies
        {
            "name": "Minimal dependencies", 
            "commands": [
                [sys.executable, "-m", "pip", "install", "psycopg2-binary", "asyncpg"],
            ]
        }
    ]
    
    for strategy in strategies:
        print(f"\n🔧 Trying: {strategy['name']}")
        
        success = True
        for cmd in strategy["commands"]:
            try:
                print(f"Running: {' '.join(cmd)}")
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print("✓ Command succeeded")
            except subprocess.CalledProcessError as e:
                print(f"❌ Command failed: {e}")
                if e.stderr:
                    print(f"Error details: {e.stderr}")
                success = False
                break
                
        if success:
            print(f"✓ {strategy['name']} completed successfully!")
            return True
            
    return False


def main():
    """Main installation routine."""
    print("🔧 Happy Path Dependency Installer")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version}")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    original_cwd = Path.cwd()
    
    try:
        import os
        os.chdir(script_dir)
        
        # Check if we need PostgreSQL development tools
        if platform.system() == "Darwin":
            print("\n🔍 Checking PostgreSQL development tools...")
            
            # Try a simple psycopg2 install to see if we need dev tools
            try:
                subprocess.run(
                    [sys.executable, "-c", "import psycopg2"], 
                    check=True, 
                    capture_output=True
                )
                print("✓ psycopg2 already available")
            except subprocess.CalledProcessError:
                print("⚠️  psycopg2 not available, checking PostgreSQL dev tools...")
                
                # Check if pg_config is available
                try:
                    subprocess.run(["pg_config", "--version"], capture_output=True, check=True)
                    print("✓ PostgreSQL development tools found")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("❌ PostgreSQL development tools not found")
                    if input("Install PostgreSQL development tools? (y/n): ").lower() == 'y':
                        if not install_postgresql_dev_tools():
                            print("⚠️  Continuing without PostgreSQL dev tools...")
        
        # Install Python packages
        print("\n📦 Installing Python packages...")
        if install_python_packages():
            print("\n🎉 All dependencies installed successfully!")
            print("\nYou can now run:")
            print("  python3 run_dev.py start")
        else:
            print("\n❌ Failed to install all dependencies.")
            print("\n🔧 Manual installation options:")
            print("  1. Install PostgreSQL (macOS): brew install postgresql@15")
            print("  2. Install psycopg2: pip install psycopg2-binary")
            print("  3. Install all requirements: pip install -r requirements.txt")
            sys.exit(1)
            
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
