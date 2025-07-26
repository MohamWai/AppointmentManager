@echo off
echo ========================================
echo   Clinic System - Desktop Shortcut Creator
echo ========================================
echo.

REM Get the current directory (where this script is located)
set SCRIPT_DIR=%~dp0

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r /c:"IPv4 Address"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%

REM Create the URL
set CLINIC_URL=http://%LOCAL_IP%:5050

echo Creating desktop shortcuts for clinic system...
echo Server IP: %LOCAL_IP%
echo URL: %CLINIC_URL%
echo.

REM Create shortcut for main clinic system
echo Creating main clinic system shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Clinic System.lnk'); $Shortcut.TargetPath = '%CLINIC_URL%'; $Shortcut.Description = 'Clinic Management System'; $Shortcut.IconLocation = 'C:\Windows\System32\shell32.dll,23'; $Shortcut.Save()"

REM Create shortcut for connection guide
echo Creating connection guide shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Clinic Connection Guide.lnk'); $Shortcut.TargetPath = '%CLINIC_URL%/connect'; $Shortcut.Description = 'Clinic System Connection Guide'; $Shortcut.IconLocation = 'C:\Windows\System32\shell32.dll,24'; $Shortcut.Save()"

echo.
echo ========================================
echo   Shortcuts Created Successfully!
echo ========================================
echo.
echo The following shortcuts have been created on your desktop:
echo.
echo 📋 "Clinic System" - Direct access to the clinic system
echo 📋 "Clinic Connection Guide" - Connection instructions for staff
echo.
echo You can now:
echo 1. Double-click "Clinic System" to access the system directly
echo 2. Share "Clinic Connection Guide" with other staff members
echo 3. Copy the URL: %CLINIC_URL% to share with others
echo.
echo Server Information:
echo - IP Address: %LOCAL_IP%
echo - Port: 5050
echo - URL: %CLINIC_URL%
echo.
pause 