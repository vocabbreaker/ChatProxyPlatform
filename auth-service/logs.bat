@echo off
REM ============================================
REM Auth Service - View Container Logs
REM ============================================
REM Displays logs from the auth-service container

echo Viewing Auth Service logs...
color 0B
echo.
echo Press Ctrl+C to exit
echo.
docker logs auth-service -f
