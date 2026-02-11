@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Flowise Debug - Environment Check
echo ========================================
echo.

set "LOG_FILE=debug_output_%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.log"
set "LOG_FILE=%LOG_FILE: =0%"

echo [INFO] Logging to: %LOG_FILE%
echo.

(
    echo ========================================
    echo Flowise Debug Report
    echo Generated: %DATE% %TIME%
    echo ========================================
    echo.
    
    echo [1] Checking if .env file exists...
    if exist .env (
        echo [OK] .env file found
    ) else (
        echo [ERROR] .env file NOT found!
    )
    echo.
    
    echo [2] Environment variables from .env file:
    echo ----------------------------------------
    type .env
    echo ----------------------------------------
    echo.
    
    echo [3] Docker Compose configuration:
    echo ----------------------------------------
    type docker-compose.yml
    echo ----------------------------------------
    echo.
    
    echo [4] Docker environment test:
    echo Testing what Docker will see...
    docker compose config
    echo.
    
    echo [5] Current Docker containers:
    docker ps -a
    echo.
    
    echo [6] Docker volumes:
    docker volume ls
    echo.
    
    echo [7] Checking for old PostgreSQL data:
    if exist "D:\DockerVolumes\flowise-postgres" (
        echo [WARNING] D:\DockerVolumes\flowise-postgres exists!
        echo This may contain old data without password.
        dir "D:\DockerVolumes\flowise-postgres"
    ) else (
        echo [OK] D:\DockerVolumes\flowise-postgres does not exist
    )
    echo.
    
    echo [8] Testing PostgreSQL password from .env:
    findstr "POSTGRES_PASSWORD" .env
    echo.
    
    echo ========================================
    echo End of Debug Report
    echo ========================================
) > "%LOG_FILE%" 2>&1

type "%LOG_FILE%"

echo.
echo ========================================
echo Debug log saved to: %LOG_FILE%
echo ========================================
echo.
pause
