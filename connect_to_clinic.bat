@echo off
echo ========================================
echo   Clinic Management System - Client
echo ========================================
echo.

REM Get server IP from user
set /p SERVER_IP="Enter the server IP address: "

REM Validate IP format (basic check)
echo %SERVER_IP% | findstr /r "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo ERROR: Invalid IP address format
    echo Please enter a valid IP address (e.g., 192.168.1.100)
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Connecting to Clinic Server
echo ========================================
echo.
echo Server IP: %SERVER_IP%
echo URL: http://%SERVER_IP%:5050
echo.
echo Opening browser...
echo.

REM Open default browser to the clinic system
start http://%SERVER_IP%:5050

echo Browser opened successfully!
echo If the page doesn't load, please check:
echo 1. Server is running on %SERVER_IP%
echo 2. Firewall allows connections on port 5050
echo 3. Both computers are on the same network
echo.
pause 