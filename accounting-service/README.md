# Accounting Service - Windows Docker Setup

Credit management service for ChatProxy Platform.

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

- **Port:** 3001
- **Database:** PostgreSQL (port 5432)
- **Purpose:** Manages user credit balances and transactions

## What This Service Does

- 💰 Tracks user credit allocations
- 📊 Records credit transactions (add/deduct/refund)
- ⏰ Manages credit expiration dates
- 🔒 Enforces credit usage limits
- 📝 Logs all credit operations

## Credit Management Tools

### Single User Operations (`quickManageCredit/`)
- `quickAddCredit.py` - Add credits to one user
- `quickCheckCredit.py` - Check user balance
- `quickRemoveAllCredit.py` - Remove all credits from one user
- `quickRemoveAllUser.py` - Remove one user completely

### Batch Operations (`quickManageCreditBatch/`)
- `quickAddCredit.py` - Add credits to multiple users
- `quickSetCredit.py` - Set exact credit amount for users
- `quickCheckCredit.py` - Check multiple user balances
- `quickRemoveAllCredit.py` - Remove all credits from multiple users
- `quickRemoveAllUser.py` - Remove multiple users

## Configuration

Single `.env` file with all settings. JWT secrets must match auth-service.

## Files

- `.env` - Environment configuration
- `docker-compose.yml` - Docker services
- `Dockerfile` - Container build
- `start.bat`, `stop.bat`, `rebuild.bat`, `logs.bat` - Management scripts
- `quickManageCredit/` - Single user credit tools
- `quickManageCreditBatch/` - Batch credit tools
- `src/` - Application source code
- `tests/` - Test files

## Backup

Old configurations stored in `backup_old_configs/` folder.
