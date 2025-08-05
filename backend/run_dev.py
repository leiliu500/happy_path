#!/usr/bin/env python3
"""
Happy Path Development Environment Manager

This script manages the development database environment using Docker.
It checks Docker installation, manages PostgreSQL containers, and provides
utilities for database operations with virtual environment support.
"""

import os
import sys
import subprocess
import time
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


class DockerManager:
    """Manages Docker operations for Happy Path development environment."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.docker_compose_path = self.project_root / "docker" / "sql"
        self.dev_compose_file = self.docker_compose_path / "docker-compose.dev.yml"
        self.venv_path = self._detect_virtual_environment()
        
    def _detect_virtual_environment(self) -> Optional[Path]:
        """Detect and return the path to the virtual environment."""
        # Check for .venv in project root (one level up from backend)
        project_root = self.project_root.parent
        venv_candidates = [
            project_root / ".venv",
            self.project_root / ".venv",
            self.project_root / "venv",
            project_root / "venv"
        ]
        
        for venv_path in venv_candidates:
            if venv_path.exists():
                # Check if it's a valid virtual environment
                python_exe = venv_path / "bin" / "python"
                if python_exe.exists():
                    return venv_path
        
        return None
    
    def _get_python_executable(self) -> str:
        """Get the Python executable to use (virtual environment if available)."""
        if self.venv_path:
            python_exe = self.venv_path / "bin" / "python"
            if python_exe.exists():
                return str(python_exe)
        
        # Fallback to system Python
        return "python3"
    
    def check_python_environment(self) -> bool:
        """Check Python environment and required packages."""
        python_exe = self._get_python_executable()
        
        try:
            # Check Python version
            result = subprocess.run(
                [python_exe, "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            python_version = result.stdout.strip()
            
            if self.venv_path:
                print(f"✓ Using virtual environment: {self.venv_path}")
                print(f"✓ Python: {python_version}")
            else:
                print(f"⚠️  Using system Python: {python_version}")
                print("  Consider creating a virtual environment for better isolation")
            
            # Check if psycopg2 is available (optional for Docker setup)
            try:
                subprocess.run(
                    [python_exe, "-c", "import psycopg2"],
                    capture_output=True,
                    check=True
                )
                print("✓ psycopg2 available for direct database connections")
            except subprocess.CalledProcessError:
                print("⚠️  psycopg2 not available (Docker connections only)")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Python environment check failed: {e}")
            return False
    
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies in the virtual environment."""
        if not self.venv_path:
            print("✗ No virtual environment found. Please create one first:")
            print("  python3 -m venv .venv")
            print("  source .venv/bin/activate")
            print("  pip install -r requirements.txt")
            return False
        
        pip_exe = self.venv_path / "bin" / "pip"
        
        try:
            print("Installing Python dependencies...")
            
            # Upgrade pip first
            subprocess.run([
                str(pip_exe), "install", "--upgrade", "pip"
            ], check=True)
            
            # Install requirements
            subprocess.run([
                str(pip_exe), "install", "-r", 
                str(self.project_root / "requirements.txt")
            ], check=True)
            
            print("✓ Python dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install dependencies: {e}")
            print("Try installing psycopg2-binary manually:")
            print(f"  {pip_exe} install psycopg2-binary")
            return False
    
    def test_database_connection(self) -> bool:
        """Test direct database connection using Python."""
        if not self.venv_path:
            print("⚠️  No virtual environment found. Skipping Python connection test.")
            return True
        
        python_exe = self._get_python_executable()
        
        try:
            # Test connection script
            test_script = '''
try:
    import psycopg2
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="happy_path_dev",
        user="happy_path_user",
        password="happy_path_dev_password",
        connect_timeout=5
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"✓ Database connection successful")
    print(f"  PostgreSQL version: {version}")
    cursor.close()
    conn.close()
except ImportError:
    print("⚠️  psycopg2 not installed - install with: pip install psycopg2-binary")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    print("  Make sure the database container is running")
'''
            
            result = subprocess.run(
                [python_exe, "-c", test_script],
                capture_output=True,
                text=True
            )
            
            print(result.stdout.strip())
            return result.returncode == 0
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Connection test failed: {e}")
            return False
        
    def check_docker_installation(self) -> bool:
        """Check if Docker and Docker Compose are installed."""
        try:
            # Check Docker
            result = subprocess.run(
                ["docker", "--version"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f"✓ Docker found: {result.stdout.strip()}")
            
            # Check Docker Compose
            result = subprocess.run(
                ["docker", "compose", "version"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f"✓ Docker Compose found: {result.stdout.strip()}")
            
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"✗ Docker or Docker Compose not found: {e}")
            print("Please install Docker Desktop from https://www.docker.com/products/docker-desktop")
            return False
    
    def check_docker_running(self) -> bool:
        """Check if Docker daemon is running."""
        try:
            subprocess.run(
                ["docker", "info"], 
                capture_output=True, 
                check=True
            )
            print("✓ Docker daemon is running")
            return True
        except subprocess.CalledProcessError:
            print("✗ Docker daemon is not running. Please start Docker Desktop.")
            return False
    
    def get_container_status(self) -> Dict[str, str]:
        """Get the status of PostgreSQL containers."""
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            containers = {}
            for line in result.stdout.strip().split('\n'):
                if line:
                    container_info = json.loads(line)
                    if 'happy_path_postgres' in container_info.get('Names', ''):
                        containers[container_info['Names']] = container_info['State']
            
            return containers
        except subprocess.CalledProcessError:
            return {}
    
    def start_dev_database(self) -> bool:
        """Start the development PostgreSQL database."""
        print("Starting development PostgreSQL database...")
        
        try:
            # Change to docker compose directory
            original_cwd = os.getcwd()
            os.chdir(self.docker_compose_path)
            
            # Start the database
            result = subprocess.run(
                ["docker", "compose", "-f", "docker-compose.dev.yml", "up", "-d"],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✓ Database container started")
            print("Waiting for database to be ready...")
            
            # Wait for database to be healthy
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    health_result = subprocess.run(
                        ["docker", "compose", "-f", "docker-compose.dev.yml", "exec", "-T", "postgres_dev", 
                         "pg_isready", "-U", "happy_path_user", "-d", "happy_path_dev"],
                        capture_output=True,
                        check=True
                    )
                    print("✓ Database is ready!")
                    return True
                except subprocess.CalledProcessError:
                    if attempt < max_attempts - 1:
                        print(f"Waiting... ({attempt + 1}/{max_attempts})")
                        time.sleep(2)
                    else:
                        print("✗ Database failed to become ready within timeout")
                        return False
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to start database: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def stop_dev_database(self) -> bool:
        """Stop the development PostgreSQL database."""
        print("Stopping development PostgreSQL database...")
        
        try:
            original_cwd = os.getcwd()
            os.chdir(self.docker_compose_path)
            
            subprocess.run(
                ["docker", "compose", "-f", "docker-compose.dev.yml", "down"],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✓ Database stopped")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to stop database: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def restart_dev_database(self) -> bool:
        """Restart the development PostgreSQL database."""
        print("Restarting development PostgreSQL database...")
        return self.stop_dev_database() and self.start_dev_database()
    
    def show_database_logs(self, follow: bool = False) -> None:
        """Show database logs."""
        try:
            original_cwd = os.getcwd()
            os.chdir(self.docker_compose_path)
            
            cmd = ["docker", "compose", "-f", "docker-compose.dev.yml", "logs"]
            if follow:
                cmd.append("-f")
            
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to show logs: {e}")
        except KeyboardInterrupt:
            print("\nLog following stopped.")
        finally:
            os.chdir(original_cwd)
    
    def connect_to_database(self) -> None:
        """Connect to the development database using psql."""
        try:
            original_cwd = os.getcwd()
            os.chdir(self.docker_compose_path)
            
            print("Connecting to development database...")
            print("Use \\q to exit the database connection.")
            
            subprocess.run([
                "docker", "compose", "-f", "docker-compose.dev.yml", "exec", 
                "postgres_dev", "psql", "-U", "happy_path_user", "-d", "happy_path_dev"
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to connect to database: {e}")
        finally:
            os.chdir(original_cwd)
    
    def reset_database(self) -> bool:
        """Reset the development database by removing volumes."""
        print("Resetting development database...")
        print("⚠️  This will destroy all data in the development database!")
        
        confirmation = input("Are you sure? Type 'yes' to confirm: ")
        if confirmation.lower() != 'yes':
            print("Reset cancelled.")
            return False
        
        try:
            original_cwd = os.getcwd()
            os.chdir(self.docker_compose_path)
            
            # Stop and remove containers and volumes
            subprocess.run([
                "docker", "compose", "-f", "docker-compose.dev.yml", "down", "-v"
            ], capture_output=True, text=True, check=True)
            
            print("✓ Database reset completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to reset database: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def show_status(self) -> None:
        """Show the current status of the development environment."""
        print("=== Happy Path Development Environment Status ===")
        
        # Check Python environment
        print("\nPython Environment:")
        self.check_python_environment()
        
        # Check Docker installation
        print("\nDocker Environment:")
        if not self.check_docker_installation():
            return
        
        # Check Docker daemon
        if not self.check_docker_running():
            return
        
        # Check container status
        containers = self.get_container_status()
        if containers:
            print("\nContainer Status:")
            for name, status in containers.items():
                status_icon = "✓" if status == "running" else "✗"
                print(f"  {status_icon} {name}: {status}")
                
            # Test database connection if container is running
            if any(status == "running" for status in containers.values()):
                print("\nDatabase Connection:")
                self.test_database_connection()
        else:
            print("\n✗ No Happy Path containers found")
        
        print(f"\nConfiguration:")
        print(f"  Docker Compose file: {self.dev_compose_file}")
        print(f"  Database connection: localhost:5433")
        print(f"  Database name: happy_path_dev")
        print(f"  Username: happy_path_user")
        if self.venv_path:
            print(f"  Virtual environment: {self.venv_path}")
        else:
            print(f"  Virtual environment: Not detected")


def main():
    """Main entry point for the development environment manager."""
    parser = argparse.ArgumentParser(
        description="Happy Path Development Environment Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_dev.py start              # Start development database
  python run_dev.py stop               # Stop development database
  python run_dev.py restart            # Restart development database
  python run_dev.py status             # Show environment status
  python run_dev.py logs               # Show database logs
  python run_dev.py logs --follow      # Follow database logs
  python run_dev.py connect            # Connect to database with psql
  python run_dev.py reset              # Reset database (destroys data)
  python run_dev.py install-deps       # Install Python dependencies
  python run_dev.py test-connection    # Test database connection
        """
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'restart', 'status', 'logs', 'connect', 'reset', 'install-deps', 'test-connection'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--follow', '-f',
        action='store_true',
        help='Follow logs (only for logs command)'
    )
    
    args = parser.parse_args()
    
    manager = DockerManager()
    
    # Execute the requested command
    if args.command == 'start':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        success = manager.start_dev_database()
        sys.exit(0 if success else 1)
        
    elif args.command == 'stop':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        success = manager.stop_dev_database()
        sys.exit(0 if success else 1)
        
    elif args.command == 'restart':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        success = manager.restart_dev_database()
        sys.exit(0 if success else 1)
        
    elif args.command == 'status':
        manager.show_status()
        
    elif args.command == 'logs':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        manager.show_database_logs(follow=args.follow)
        
    elif args.command == 'connect':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        manager.connect_to_database()
        
    elif args.command == 'reset':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        success = manager.reset_database()
        sys.exit(0 if success else 1)
        
    elif args.command == 'install-deps':
        success = manager.install_python_dependencies()
        sys.exit(0 if success else 1)
        
    elif args.command == 'test-connection':
        if not manager.check_docker_installation() or not manager.check_docker_running():
            sys.exit(1)
        success = manager.test_database_connection()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
