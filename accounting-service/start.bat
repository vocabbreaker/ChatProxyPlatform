@echo off
REM ============================================
REM Accounting Service - Start Docker Containers
REM ============================================
REM Starts the accounting service with PostgreSQL

echo Starting Accounting Service Docker containers...
color 0A

REM Check if containers are already running
docker ps | findstr "accounting-service" >nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [INFO] Containers are already running!
    echo.
    goto :show_info
)

echo.
echo Starting containers...
docker compose up -d

echo.
echo [SUCCESS] Docker startup complete!
echo.

:show_info
echo ============================================
echo Service Endpoints:
echo ============================================
echo Accounting API:  http://localhost:3001
echo PostgreSQL:      localhost:5432
echo ============================================
echo.
pause
