# Auth Service - Windows Docker Deployment

This folder contains a clean, consolidated setup for Windows Docker deployment.

## Quick Start

```batch
# Start containers
start.bat

# Stop containers
stop.bat

# Rebuild after code changes
rebuild.bat

# View logs
logs.bat
```

## Files Structure

### Essential Files
- **`.env`** - Single environment configuration
- **`docker-compose.dev.yml`** - Docker services configuration
- **`Dockerfile.dev`** - Development container image
- **`Dockerfile`** - Production container image

### Management Scripts
- **`start.bat`** - Start all containers
- **`stop.bat`** - Stop all containers
- **`rebuild.bat`** - Rebuild and restart containers
- **`logs.bat`** - View container logs

### Admin Tools
- **`quickCreateAdminPy/`** - User management scripts

## Service Endpoints

- **Auth Service:** http://localhost:3000
- **MongoDB:** localhost:27017
- **MailHog UI:** http://localhost:8025
- **MailHog SMTP:** localhost:1025

## Admin Account

Default credentials (change in production):
- **Username:** admin
- **Email:** admin@example.com
- **Password:** admin@admin

## Backup Files

Old configuration files are in `backup_old_configs/` folder.
