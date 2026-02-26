@echo off
REM ============================================================================
REM ChatProxyPlatform - Automated Setup with Prerequisites Check
REM ============================================================================
REM
REM This script:
REM 1. Checks for Docker, Node.js, Python, Git
REM 2. Installs missing prerequisites automatically
REM 3. Handles Docker Desktop + WSL2 installation and reboot
REM 4. Runs the Python setup script
REM
REM Usage: automated_setup.bat
REM ============================================================================

setlocal enabledelayedexpansion

REM Ensure we are in the script directory
cd /d "%~dp0"

echo.
echo ================================================================================
echo ChatProxyPlatform - Automated Setup
echo ================================================================================
echo.

REM ============================================================================
REM Run Python Setup Script
REM ============================================================================
echo Starting automated setup...
echo.

REM Check if automated_setup.py exists
if not exist "%~dp0automated_setup.py" (
    echo [ERROR] automated_setup.py not found in current directory
    echo.
    echo Please make sure you're running this from the ChatProxyPlatform root directory
    echo.
    pause
    exit /b 1
)

REM Run the Python setup script
echo.
python "%~dp0automated_setup.py"

REM Capture exit code
set EXIT_CODE=%errorlevel%

echo.
if %EXIT_CODE% equ 0 (
    echo ================================================================================
    echo Setup completed successfully!
    echo ================================================================================
    echo.
    echo Access your services:
    echo   - Bridge UI: http://localhost:8080
    echo   - Flowise: http://localhost:3002
    echo   - MailHog: http://localhost:8025
    echo.
    echo Default admin credentials:
    echo   - Email: admin@example.com
    echo   - Password: Admin123!
    echo.
) else (
    echo ================================================================================
    echo Setup encountered errors. Please review the output above.
    echo ================================================================================
)

echo.
echo Press any key to exit...
pause >nul

exit /b %EXIT_CODE%
