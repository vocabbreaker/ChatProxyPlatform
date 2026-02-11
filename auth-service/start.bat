@echo off
REM ============================================
REM Auth Service - Start Docker Containers
REM ============================================
REM Starts the auth service with MongoDB and MailHog

echo Starting Auth Service Docker containers...
color 0A

REM Check if containers are already running
docker ps | findstr "auth-service" >nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [INFO] Containers are already running!
    echo.
    goto :show_info
)

echo.
echo Starting containers...
docker compose -f docker-compose.dev.yml up -d

echo.
echo [SUCCESS] Docker startup complete!
echo.

:show_info
echo ============================================
echo Service Endpoints:
echo ============================================
echo Auth Service:  http://localhost:3000
echo MailHog UI:    http://localhost:8025
echo MongoDB:       localhost:27017
echo ============================================
echo.
pause
