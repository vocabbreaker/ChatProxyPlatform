@echo off
REM =============================================================
REM Complete User and Credit Management
REM 
REM What this does:
REM 1. Creates new users (action=create in CSV)
REM 2. Deletes users (action=delete in CSV)  
REM 3. Verifies users so they can login
REM 4. Initializes users in accounting system
REM 5. Sets credits for all users
REM
REM Usage: Just edit users.csv and run this file
REM =============================================================

echo.
echo ============================================================
echo Complete User and Credit Sync
echo ============================================================
echo.
echo This will:
echo  - Create/delete users from CSV
echo  - Verify all users
echo  - Initialize users in accounting
echo  - Set credits for all users
echo.
pause

echo.
echo [Step 1/5] Creating/deleting users...
echo.
python manage_users_csv.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to manage users
    pause
    exit /b 1
)

echo.
echo [Step 2/5] Verifying users (so they can login)...
echo.
python verify_all_users.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to verify users
    pause
    exit /b 1
)

echo.
echo [Step 3/5] Initializing users in accounting system...
echo.
python init_users_in_accounting.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to initialize users
    pause
    exit /b 1
)

echo.
echo [Step 4/5] Setting credits for all users...
echo.
python sync_credits.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to sync credits
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS! All users and credits synchronized
echo ============================================================
echo.
pause
