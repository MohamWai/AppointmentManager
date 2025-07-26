@echo off
echo ========================================
echo   Clinic Management System - Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if PostgreSQL is running
echo Checking database connection...
python -c "import psycopg; psycopg.connect('postgresql://clinicuser:admin@localhost/clinicdb')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot connect to PostgreSQL database
    echo Please ensure PostgreSQL is running and database is set up
    pause
    exit /b 1
)

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r /c:"IPv4 Address"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%

echo.
echo ========================================
echo   Starting Clinic Management System
echo ========================================
echo.
echo Local Access:  http://localhost:5050
echo Network Access: http://%LOCAL_IP%:5050
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause 