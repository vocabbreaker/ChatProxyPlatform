@echo off
echo ========================================
echo Starting Flowise with PostgreSQL
echo ========================================
echo.

docker compose --profile postgres up -d

echo.
echo ========================================
echo Flowise is starting with PostgreSQL...
echo Access at: http://localhost:3000
echo PostgreSQL Port: 5433
echo ========================================
echo.
echo To view logs: docker logs flowise -f
echo To stop: docker compose --profile postgres down
echo.
