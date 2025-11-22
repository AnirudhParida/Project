@echo off
REM Quick start script for OS Agent

echo Starting OS Agent in VOICE mode...
echo.
echo Say "exit" to quit
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the agent
python main.py

pause
