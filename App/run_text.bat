@echo off
REM Quick start script for OS Agent in text mode

echo Starting OS Agent in TEXT mode...
echo.
echo Type "exit" to quit
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run the agent in text mode
python main.py --mode text

pause
