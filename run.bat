@echo off
TITLE Morphological Transducer Launcher
echo Starting Morphological Transducer...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python to run the local server.
    pause
    exit /b
)

:: Navigate to project directory
cd /d "%~dp0main\project"

:: Start the server in a new minimized window
start /min "Morphological Server" python -m http.server 8181

:: Wait a moment for server to start
timeout /t 2 /nobreak >nul

:: Open the browser
start http://localhost:8181

echo Server is running at http://localhost:8181
echo Press any key to stop the server and exit...
pause

:: Kill the python process started on port 8181
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8181') do taskkill /f /pid %%a >nul 2>&1

exit
