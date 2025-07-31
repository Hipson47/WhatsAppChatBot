@echo off
cls
echo Starting AI Chatbot Environment...

:: Check 1: Verify that the .env file exists
if not exist .env (
    echo.
    echo ERROR: .env file not found!
    echo Please create a '.env' file by copying '.env.example' and filling in your API keys.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [OK] .env file found.

:: Check 2: Verify that GOOGLE_APPLICATION_CREDENTIALS path is set in the .env file
findstr /i "GOOGLE_APPLICATION_CREDENTIALS" .env > nul
if %errorlevel% neq 0 (
    echo.
    echo WARNING: GOOGLE_APPLICATION_CREDENTIALS is not set in your .env file.
    echo The knowledge base ingestion will likely fail.
    echo Please follow the instructions in README.md to set it up.
    echo Press any key to continue anyway, or close this window to fix it...
    pause
) else (
    echo [OK] GOOGLE_APPLICATION_CREDENTIALS variable found in .env file.
)

:: Check 3: Check if the vector_store directory exists
if exist vector_store (
    echo.
    echo Knowledge base found. Do you want to rebuild it? (y/n)
    set /p rebuild_choice=
    if /i "%rebuild_choice%"=="y" (
        echo Rebuilding knowledge base...
        python ingest.py
    ) else (
        echo Skipping knowledge base rebuild.
    )
) else (
    echo.
    echo Knowledge base not found. Building it for the first time...
    python ingest.py
)

echo.
echo Starting the Telegram Bot...
echo Press CTRL+C in this window to stop the bot.
python main.py