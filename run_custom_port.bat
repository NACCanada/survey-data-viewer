@echo off
REM Survey Data Viewer - Custom Port Launcher
REM Edit the PORT number below to change which port the app uses

echo ========================================
echo Survey Data Viewer - Custom Port
echo ========================================
echo.

REM Set custom port (change 9000 to your preferred port)
set PORT=9000

echo Starting on port %PORT%...
echo.
echo Browser will open at: http://localhost:%PORT%
echo.

REM Run the application
SurveyDataViewer.exe

pause
