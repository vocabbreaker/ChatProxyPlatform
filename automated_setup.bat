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
REM Step 1: Check Prerequisites
REM ============================================================================
echo [Step 1/2] Checking prerequisites...
echo.

set NEED_INSTALL=0
set NEED_REBOOT=0
set MISSING_LIST=

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [!] Python is NOT installed
    set NEED_INSTALL=1
    set MISSING_LIST=!MISSING_LIST! Python
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   [OK] %%i
)

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo   [!] Node.js is NOT installed
    set NEED_INSTALL=1
    set MISSING_LIST=!MISSING_LIST! Node.js
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do echo   [OK] Node.js %%i
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo   [!] npm is NOT installed
) else (
    for /f "tokens=*" %%i in ('npm --version 2^>^&1') do echo   [OK] npm %%i
)

REM Check Docker
echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo   [!] Docker is NOT installed
    set NEED_INSTALL=1
    set NEED_REBOOT=1
    set MISSING_LIST=!MISSING_LIST! Docker
) else (
    for /f "tokens=*" %%i in ('docker --version 2^>^&1') do echo   [OK] %%i
    
    REM Check if Docker daemon is running
    docker ps >nul 2>&1
    if errorlevel 1 (
        echo   [!] Docker Desktop is not running - Please start Docker Desktop
        echo.
        echo       - Open Docker Desktop from Start Menu
        echo       - Wait for green checkmark in system tray
        echo       - Then press any key to continue...
        pause >nul
    ) else (
        echo   [OK] Docker daemon is running
    )
)

REM Check Git
echo Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo   [!] Git is NOT installed (optional)
    set MISSING_LIST=!MISSING_LIST! Git
) else (
    for /f "tokens=*" %%i in ('git --version 2^>^&1') do echo   [OK] %%i
)

echo.

REM ============================================================================
REM Step 2: Install Missing Prerequisites
REM ============================================================================
if %NEED_INSTALL%==1 (
    echo ================================================================================
    echo Installing Missing Prerequisites
    echo ================================================================================
    echo.
    echo Missing:%MISSING_LIST%
    echo.
    
    REM Check if winget is available
    winget --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] winget is not available on this system
        echo.
        echo Please manually install the missing software:
        if defined MISSING_LIST echo   - Python 3.12: https://www.python.org/downloads/
        if defined MISSING_LIST echo   - Node.js LTS: https://nodejs.org/
        if defined MISSING_LIST echo   - Docker Desktop: https://www.docker.com/products/docker-desktop/
        if defined MISSING_LIST echo   - Git: https://git-scm.com/downloads/
        echo.
        echo Then run this script again.
        pause
        exit /b 1
    )
    
    echo Installing prerequisites using winget...
    echo This may take 5-10 minutes...
    echo.
    
    REM Install Python if missing
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Installing Python 3.12...
        winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements --silent
    )
    
    REM Install Node.js if missing
    node --version >nul 2>&1
    if errorlevel 1 (
        echo Installing Node.js LTS...
        winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements --silent
    )
    
    REM Install Docker if missing
    docker --version >nul 2>&1
    if errorlevel 1 (
        echo Installing Docker Desktop...
        echo NOTE: Docker requires WSL2 and may require a system reboot
        winget install -e --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
    )
    
    REM Install Git if missing
    git --version >nul 2>&1
    if errorlevel 1 (
        echo Installing Git...
        winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements --silent
    )
    
    echo.
    echo ================================================================================
    echo Prerequisites Installation Complete
    echo ================================================================================
    echo.
    
    if %NEED_REBOOT%==1 (
        echo [IMPORTANT] Docker Desktop was installed and requires:
        echo.
        echo   1. RESTART YOUR COMPUTER to enable WSL2
        echo   2. After restart, open Docker Desktop from Start Menu
        echo   3. Wait for Docker to fully start (green checkmark in system tray)
        echo   4. Run this script again: automated_setup.bat
        echo.
        echo ================================================================================
        echo.
        choice /C YN /M "Restart computer now"
        if !errorlevel!==1 (
            echo Restarting in 10 seconds... (Press Ctrl+C to cancel)
            timeout /t 10
            shutdown /r /t 0
            exit /b 0
        ) else (
            echo.
            echo Please restart manually, then run automated_setup.bat again
            pause
            exit /b 0
        )
    ) else (
        echo [IMPORTANT] Please restart this terminal (close and reopen) for PATH changes
        echo Then run this script again: automated_setup.bat
        echo.
        pause
        exit /b 0
    )
)

REM ============================================================================
REM Step 3: Run Python Setup Script
REM ============================================================================
echo [Step 2/2] Running automated setup...
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

REM Verify Docker is running before continuing
docker ps >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker Desktop is not running!
    echo.
    echo Please:
    echo   1. Open Docker Desktop from Start Menu
    echo   2. Wait for it to fully start (green checkmark in system tray)
    echo   3. Then press any key to continue...
    echo.
    pause >nul
)

REM Run the Python setup script
echo Starting ChatProxyPlatform setup...
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
