@echo off
echo ========================================
echo OS Agent - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found!
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [4/4] Installing dependencies...
echo This may take a few minutes...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
echo 2. Copy .env.example to .env
echo 3. Add your API key to .env
echo.
echo NOTE: If PyAudio installation failed, you need to:
echo - Download the .whl file from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo - Install with: pip install path\to\PyAudio-file.whl
echo.
echo To run the agent:
echo   python main.py              (voice mode)
echo   python main.py --mode text  (text mode)
echo.
pause
