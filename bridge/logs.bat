@echo off
REM =============================================================
REM Bridge UI - View Docker Logs
REM =============================================================

echo.
echo ============================================================
echo Bridge UI Docker Logs
echo ============================================================
echo.
echo Press Ctrl+C to exit log viewer
echo.

docker compose logs -f bridge-ui
