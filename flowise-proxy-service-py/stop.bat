@echo off
echo ===================================================
echo =========  Stopping Flowise Proxy
echo ===================================================
echo.

docker compose down

if %ERRORLEVEL% NEQ 0 (
    echo ===================================================
    echo =========  ERROR: Failed to stop Flowise Proxy
    echo ===================================================
    pause
    exit /b 1
)

echo.
echo ===================================================
echo =========  Flowise Proxy stopped successfully
echo ===================================================
pause
