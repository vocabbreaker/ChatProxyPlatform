@echo off
REM ============================================
REM CSV User Management - Admin Rights Required
REM ============================================
REM Creates and deletes users from users.csv file

echo ============================================
echo CSV User Management Script
echo ============================================
echo.

REM Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script requires Administrator privileges!
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [OK] Running with Administrator privileges
echo.

REM Check if users.csv exists
if not exist "users.csv" (
    echo [INFO] users.csv not found. Creating from template...
    if exist "users_template.csv" (
        copy "users_template.csv" "users.csv"
        echo [SUCCESS] Created users.csv from template
        echo.
        echo Please edit users.csv with your user data and run this script again.
        echo.
        notepad users.csv
        pause
        exit /b 0
    ) else (
        echo [ERROR] Template file users_template.csv not found!
        pause
        exit /b 1
    )
)

echo [INFO] Found users.csv file
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

REM Run the CSV management script
echo [INFO] Processing users from CSV file...
echo.
python manage_users_csv.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

echo.
echo ============================================
echo Script completed
echo Check user_management.log for details
echo ============================================
pause
