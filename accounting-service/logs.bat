@echo off
REM ============================================
REM Accounting Service - View Container Logs
REM ============================================
REM Displays logs from the accounting-service container

echo Viewing Accounting Service logs...
color 0B
echo.
echo Press Ctrl+C to exit
echo.
docker logs accounting-service -f
