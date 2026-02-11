@echo off
REM ============================================
REM Auth Service - Rebuild Docker Containers
REM ============================================
REM Stops, rebuilds, and restarts all containers
REM Use this when you've made code or configuration changes

echo Rebuilding Auth Service Docker containers...
color 0E

echo.
echo [1/4] Stopping containers...
docker compose -f docker-compose.dev.yml down

echo.
echo [2/4] Rebuilding images with no cache...
docker compose -f docker-compose.dev.yml build --no-cache

echo.
echo [3/4] Starting containers...
docker compose -f docker-compose.dev.yml up -d

echo.
echo [4/4] Complete!
echo.
echo ============================================
echo Service Endpoints:
echo ============================================
echo Auth Service:  http://localhost:3000
echo MailHog UI:    http://localhost:8025
echo MongoDB:       localhost:27017
echo ============================================
echo.
echo TIP: Check logs with: docker logs auth-service -f
echo.
pause
