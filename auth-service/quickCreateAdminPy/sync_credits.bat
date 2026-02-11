@echo off
REM ============================================
REM Sync User Credits from CSV
REM ============================================
REM Reads users.csv and sets credit amounts for each user
REM Run this anytime to sync credits to CSV values

echo ============================================
echo Credit Sync from CSV
echo ============================================
echo.

REM Check if users.csv exists
if not exist "users.csv" (
    echo [ERROR] users.csv not found!
    echo.
    echo Please ensure users.csv exists with email and credits columns.
    echo.
    pause
    exit /b 1
)

echo [INFO] Found users.csv
echo.

REM Check if Python virtual environment exists
if not exist "venv\" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo [INFO] Installing required packages...
pip install --quiet --upgrade pip
pip install --quiet requests
echo [SUCCESS] Packages installed
echo.

REM Run the credit sync script
echo [INFO] Syncing credits from CSV...
echo.
python sync_credits.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
pause
