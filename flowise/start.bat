@echo off
echo ========================================
echo Starting Flowise with Docker Compose
echo ========================================
echo.

docker compose up -d

echo.
echo ========================================
echo Flowise is starting...
echo Access at: http://localhost:3000
echo ========================================
echo.
echo To view logs: docker logs flowise -f
echo To stop: docker compose down
echo.
