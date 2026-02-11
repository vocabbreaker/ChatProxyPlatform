@echo off
REM =============================================================
REM Bridge UI - Start Docker Container
REM =============================================================

echo.
echo ============================================================
echo Starting Bridge UI Docker Container
echo ============================================================
echo.

docker compose up -d --build

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS! Bridge UI is running
    echo ============================================================
    echo.
    echo Access the UI at: http://localhost:3082
    echo.
    echo Container: bridge-ui
    echo Network: bridge-network
    echo.
    echo Management commands:
    echo   - Stop:  docker compose down
    echo   - Logs:  docker compose logs -f bridge-ui
    echo   - Status: docker ps
    echo.
) else (
    echo.
    echo ============================================================
    echo ERROR: Failed to start Bridge UI
    echo ============================================================
    echo.
    echo Please check Docker Desktop is running
    echo.
)

pause
