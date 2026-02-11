@echo off
REM ============================================
REM Auth Service - Stop Docker Containers
REM ============================================
REM Stops all auth service containers

echo Stopping Auth Service Docker containers...
color 0C

echo.
docker compose -f docker-compose.dev.yml down

echo.
echo [SUCCESS] All containers stopped!
echo.
echo TIP: To also remove volumes (database data), run:
echo      docker compose -f docker-compose.dev.yml down -v
echo.
pause
