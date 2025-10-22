@echo off
REM Simple batch file to start the production server

echo Starting Mail Tracker Production Server...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    python run_server.py
) else (
    echo Virtual environment not found!
    echo Please create one with: python -m venv venv
    echo Then install requirements: pip install -r requirements.txt
    pause
)