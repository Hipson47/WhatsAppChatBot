@echo off

echo Checking for virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Installing dependencies, this may take a moment...
.\venv\Scripts\pip.exe install -r backend/requirements.txt

echo Starting the server...
.\venv\Scripts\uvicorn.exe backend.app:app --host 0.0.0.0 --port 8000

pause 