@echo off
REM =============================================================
REM Bridge UI - Rebuild Docker Container
REM =============================================================

echo.
echo ============================================================
echo Rebuilding Bridge UI Docker Container
echo ============================================================
echo.
echo This will:
echo  1. Stop the current container
echo  2. Remove old images
echo  3. Rebuild from Dockerfile
echo  4. Start the new container
echo.

pause

echo.
echo Stopping container...
docker compose down

echo.
echo Rebuilding and starting...
docker compose up -d --build --force-recreate

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS! Bridge UI rebuilt and running
    echo ============================================================
    echo.
    echo Access at: http://localhost:3082
    echo.
) else (
    echo.
    echo ERROR: Rebuild failed
    echo.
)

pause
