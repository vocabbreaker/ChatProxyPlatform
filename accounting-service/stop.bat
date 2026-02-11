@echo off
REM ============================================
REM Accounting Service - Stop Docker Containers
REM ============================================
REM Stops all accounting service containers

echo Stopping Accounting Service Docker containers...
color 0C

echo.
docker compose down

echo.
echo [SUCCESS] All containers stopped!
echo.
echo TIP: To also remove volumes (database data), run:
echo      docker compose down -v
echo.
pause
