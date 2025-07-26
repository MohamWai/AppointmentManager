@echo off
echo ========================================
echo   Clinic Management System - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python is installed ✓
python --version

REM Check if PostgreSQL is installed
echo.
echo Checking PostgreSQL installation...
psql --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL is not installed or not in PATH
    echo.
    echo Please install PostgreSQL from https://postgresql.org/download/windows/
    echo After installation, you'll need to create the database manually
    echo.
    echo Press any key to continue with Python setup only...
    pause
)

echo PostgreSQL is installed ✓
psql --version

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created ✓
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed ✓

REM Test database connection
echo.
echo Testing database connection...
python -c "import psycopg; psycopg.connect('postgresql://clinicuser:admin@localhost/clinicdb')" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Cannot connect to PostgreSQL database
    echo.
    echo Please ensure:
    echo 1. PostgreSQL is running
    echo 2. Database 'clinicdb' exists
    echo 3. User 'clinicuser' with password 'admin' exists
    echo.
    echo To create the database, run these commands in psql:
    echo CREATE DATABASE clinicdb;
    echo CREATE USER clinicuser WITH PASSWORD 'admin';
    echo GRANT ALL PRIVILEGES ON DATABASE clinicdb TO clinicuser;
    echo.
    echo Press any key to continue...
    pause
) else (
    echo Database connection successful ✓
)

REM Create desktop shortcut
echo.
echo Creating desktop shortcut...
if exist "create_desktop_shortcut.bat" (
    call create_desktop_shortcut.bat
    echo Desktop shortcut created ✓
) else (
    echo Desktop shortcut script not found
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the clinic system:
echo 1. Double-click start_clinic_server.bat
echo 2. Or run: venv\Scripts\activate.bat && python app.py
echo.
echo Access the system at: http://localhost:5050
echo.
echo For network access, configure Windows Firewall to allow port 5050
echo.
pause 