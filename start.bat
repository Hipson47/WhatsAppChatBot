@echo off
TITLE WhatsApp Bot Launcher

ECHO --- Starting Backend Server in a new window...
START "Backend Server (Docker)" docker-compose up --build

ECHO --- Starting Ngrok Tunnel in a new window...
ECHO --- Please wait a few seconds for the window to appear.
TIMEOUT /T 3 /NOBREAK >nul
START "Ngrok Tunnel" .\ngrok.exe http 8000

echo.
ECHO --- Both services have been launched in separate windows. ---
ECHO You can close this window now.
ECHO To stop the services, simply close the other two windows ("Backend Server" and "Ngrok Tunnel").
pause 