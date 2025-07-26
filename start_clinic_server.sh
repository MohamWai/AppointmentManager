#!/bin/bash

echo "========================================"
echo "  Clinic Management System - Server"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if PostgreSQL is running
echo "Checking database connection..."
python3 -c "import psycopg; psycopg.connect('postgresql://clinicuser:admin@localhost/clinicdb')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Cannot connect to PostgreSQL database"
    echo "Please ensure PostgreSQL is running and database is set up"
    exit 1
fi

# Get local IP address (macOS compatible)
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n1)

echo
echo "========================================"
echo "  Starting Clinic Management System"
echo "========================================"
echo
echo "Local Access:  http://localhost:5050"
echo "Network Access: http://$LOCAL_IP:5050"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the Flask application
python3 app.py 