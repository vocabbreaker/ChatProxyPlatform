@echo off
REM =============================================================
REM Bridge UI - Stop Docker Container
REM =============================================================

echo.
echo ============================================================
echo Stopping Bridge UI Docker Container
echo ============================================================
echo.

docker compose down

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo Bridge UI stopped successfully
    echo ============================================================
    echo.
) else (
    echo.
    echo ERROR: Failed to stop Bridge UI
    echo.
)

pause
