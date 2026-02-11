@echo off
REM ============================================
REM Accounting Service - Rebuild Docker Containers
REM ============================================
REM Stops, rebuilds, and restarts all containers

echo Rebuilding Accounting Service Docker containers...
color 0E

echo.
echo [1/4] Stopping containers...
docker compose down

echo.
echo [2/4] Rebuilding images with no cache...
docker compose build --no-cache

echo.
echo [3/4] Starting containers...
docker compose up -d

echo.
echo [4/4] Complete!
echo.
echo ============================================
echo Service Endpoints:
echo ============================================
echo Accounting API:  http://localhost:3001
echo PostgreSQL:      localhost:5432
echo ============================================
echo.
echo TIP: Check logs with: docker logs accounting-service -f
echo.
pause
