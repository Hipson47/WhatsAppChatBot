@echo off
TITLE WhatsApp Bot - LOCAL TEST

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment and installing dependencies...
call .\venv\Scripts\activate.bat
pip install -r backend\requirements.txt

echo ---
echo Starting local server on http://localhost:8000
echo This will NOT connect to Twilio unless you run ngrok separately.
echo This is for local testing of the API logic.
echo ---

python backend/app.py
pause 