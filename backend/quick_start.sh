#!/bin/bash

# Happy Path Quick Start Script
# This script performs the initial setup and starts the development environment

echo "🚀 Happy Path Development Environment Quick Start"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "run_dev.py" ]; then
    echo "❌ Error: run_dev.py not found. Please run this script from the backend directory."
    exit 1
fi

echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi
echo "✅ Python 3 found"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo "✅ Docker found"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "✅ Docker is running"

echo ""
echo "🗄️  Setting up development environment..."
python3 run_dev.py setup

if [ $? -eq 0 ]; then
    echo ""
    echo "🗄️  Starting development database..."
    python3 run_dev.py start
else
    echo ""
    echo "❌ Environment setup failed. Please check the error messages above."
    echo ""
    echo "🔧 Manual setup options:"
    echo "  1. Install PostgreSQL development libraries:"
    echo "     brew install postgresql@15"
    echo ""
    echo "  2. Install Python dependencies:"
    echo "     pip install psycopg2-binary"
    echo ""
    echo "  3. Try again:"
    echo "     python3 run_dev.py setup"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Success! Your development environment is ready!"
    echo ""
    echo "📊 Environment Details:"
    echo "  Database: happy_path_dev"
    echo "  Host: localhost"
    echo "  Port: 5433"
    echo "  Username: happy_path_user"
    echo "  Password: happy_path_dev_password"
    echo ""
    echo "🔧 Useful Commands:"
    echo "  python3 run_dev.py status    # Check status"
    echo "  python3 run_dev.py connect   # Connect to database"
    echo "  python3 run_dev.py logs      # View logs"
    echo "  python3 run_dev.py stop      # Stop database"
    echo ""
    echo "📚 For more information, see docker/sql/README.md"
else
    echo ""
    echo "❌ Failed to start development environment."
    echo "Please check the error messages above and try again."
    exit 1
fi
