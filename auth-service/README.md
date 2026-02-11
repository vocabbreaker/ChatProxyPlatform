# Auth Service - Windows Docker Setup

Simple authentication service for ChatProxy Platform.

## Quick Start

```batch
# Start service
start.bat

# Stop service
stop.bat

# Rebuild after changes
rebuild.bat

# View logs
logs.bat
```

## Service Info

- **Port:** 3000
- **Database:** MongoDB (port 27017)
- **Email Testing:** MailHog UI at http://localhost:8025

## Admin Management

```batch
cd quickCreateAdminPy

# Create admin account (first time)
setup_and_run.bat

# Manage users via CSV (requires admin rights)
# Right-click and "Run as administrator"
manage_users_admin.bat

# List all users
list_users.bat

# Test login
test_login.bat
```

## Configuration

Single `.env` file with all settings. JWT secrets must match across all services.

## CSV User Management

Bulk create/delete teachers and students:

1. Edit `quickCreateAdminPy\users.csv`
2. Right-click `manage_users_admin.bat` → Run as administrator
3. Check `user_management.log` for results

See `quickCreateAdminPy\CSV_USER_MANAGEMENT.md` for details.

## Files

- `.env` - Environment configuration
- `docker-compose.dev.yml` - Docker services
- `Dockerfile` - Container build
- `start.bat`, `stop.bat`, `rebuild.bat`, `logs.bat` - Management scripts
- `quickCreateAdminPy/` - User management tools
- `src/` - Application source code
- `tests/` - Test files

## Backup

Old configurations and documentation stored in:
- `backup_old_configs/` - Old scripts, docs, and configs
- `backup_env/` - Old environment files
