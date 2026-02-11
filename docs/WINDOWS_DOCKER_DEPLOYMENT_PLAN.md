# Windows Docker Deployment Plan

## Overview
This document provides a comprehensive plan for deploying the three-service architecture on Windows using Docker only.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Files Audit](#environment-files-audit)
3. [Files That Can Be Removed](#files-that-can-be-removed)
4. [Files That Must Be Kept](#files-that-must-be-kept)
5. [Environment Configuration Plan](#environment-configuration-plan)
6. [Docker Deployment Strategy](#docker-deployment-strategy)
7. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
8. [Verification Checklist](#verification-checklist)

---

## Prerequisites

### Required Software
- [ ] **Docker Desktop for Windows** (latest version)
  - Enable WSL 2 backend
  - Allocate at least 8GB RAM to Docker
  - Allocate at least 4 CPU cores
- [ ] **Git for Windows** (for cloning/pulling updates)
- [ ] **Text Editor** (VS Code, Notepad++, etc.)
- [ ] **Windows Terminal** or PowerShell (optional but recommended)

### System Requirements
- Windows 10/11 (64-bit)
- 16GB RAM minimum (32GB recommended)
- 50GB free disk space
- Internet connection for pulling Docker images

---

## Environment Files Audit

### Current .env Files Found

#### 1. Auth Service
| File | Location | Status | Action |
|------|----------|--------|--------|
| `.env.development` | `auth-service/` | ✅ Exists | **Keep** - Use as template for .env |
| `.env.production` | `auth-service/` | ✅ Exists | **Keep** - Reference for production values |
| `.env.samehost` | `auth-service/` | ✅ Exists | **Optional** - Can remove if not using |
| `.env` | `auth-service/` | ❌ Not in repo | **Create** - From .env.development |

#### 2. Flowise Proxy Service
| File | Location | Status | Action |
|------|----------|--------|--------|
| `.env.example` | `flowise-proxy-service-py/` | ✅ Exists | **Keep** - Template file |
| `.env` | `flowise-proxy-service-py/` | ❌ Not in repo | **Create** - From .env.example |
| `.env.test` | `flowise-proxy-service-py/` | ⚠️ Gitignored | **Optional** - For testing |

#### 3. Accounting Service
| File | Location | Status | Action |
|------|----------|--------|--------|
| `.env.example` | `accounting-service/` | ✅ Exists | **Keep** - Template file |
| `.env` | `accounting-service/` | ❌ Not in repo | **Create** - From .env.example |

---

## Files That Can Be Removed

### ❌ Linux-Specific Shell Scripts (.sh files)

#### Auth Service - 11 files
```
auth-service/setup_linux.sh
auth-service/rebuild_docker_samehost_linux.sh
auth-service/rebuild_docker_samehost.sh
auth-service/rebuild_docker.sh
auth-service/check_network.sh
auth-service/tests/install.sh
auth-service/tests/start.sh
auth-service/quickCreateAdminPy/create_users.sh
auth-service/quickCreateAdminPy/list_users.sh
auth-service/quickCreateAdminPySamehost/quickSet.sh
auth-service/quickCreateAdminPySamehost/list_users.sh
```

#### Flowise Proxy Service - 10 files
```
flowise-proxy-service-py/quick_view_messages.sh
flowise-proxy-service-py/quick_update_docker.sh
flowise-proxy-service-py/run-migrations-docker.sh
flowise-proxy-service-py/rebuild-docker-test.sh
flowise-proxy-service-py/migrate_production.sh
flowise-proxy-service-py/migrate-production.sh
flowise-proxy-service-py/migrate-production-simple.sh
flowise-proxy-service-py/update_docker_code.sh
flowise-proxy-service-py/docker_update_commands.sh
flowise-proxy-service-py/analyze_docker_setup.sh
```

#### Accounting Service - 2 files
```
accounting-service/rebuild-docker-rebuild-volume.sh
accounting-service/start-docker.sh
accounting-service/fix_db_schema.ps1
```

**Total: ~23 shell scripts can be removed for Windows-only deployment**

### ❌ Unnecessary Docker Compose Files

#### Auth Service
```
auth-service/docker-compose.samehost.yml  (if not using samehost mode)
auth-service/docker-compose.prod.yml      (keep if deploying to production)
```

#### Flowise Proxy Service
```
flowise-proxy-service-py/docker-compose.test.yml       (testing only)
flowise-proxy-service-py/docker-compose.dbonly.yml     (DB testing only)
flowise-proxy-service-py/docker-compose.linux.yml      (Linux-specific)
```

#### Accounting Service
```
accounting-service/docker-compose.linux.yml    (Linux-specific)
accounting-service/docker-compose.debug.yml    (debugging only)
```

### ❌ Optional Documentation/Guide Files

These can be removed or moved to a separate docs archive:
```
flowise-proxy-service-py/CHAT_API_REFACTORING.md
flowise-proxy-service-py/COLLECTION_SETUP_GUIDE.md
flowise-proxy-service-py/DELETE_CHAT_HISTORY_USAGE.md
flowise-proxy-service-py/DOCKER_UPDATE_GUIDE.md
flowise-proxy-service-py/ENHANCED_MIGRATION_GUIDE.md
flowise-proxy-service-py/FILE_STORAGE_BEST_PRACTICES.md
flowise-proxy-service-py/FRONTEND_INTEGRATION_GUIDE.md
flowise-proxy-service-py/FRONTEND_QUICK_REFERENCE.md
flowise-proxy-service-py/IMAGE_RENDERING_MIGRATION_GUIDE.md
flowise-proxy-service-py/MIGRATION_GUIDE.md
flowise-proxy-service-py/MIGRATION_QUICK_GUIDE.md
flowise-proxy-service-py/MONGODB_QUERIES.md
flowise-proxy-service-py/TYPESCRIPT_INTEGRATION_GUIDE.md
flowise-proxy-service-py/TYPESCRIPT_QUICK_REFERENCE.md
auth-service/DOCUMENTATION.md
auth-service/ENDPOINT_CORRECTION_UPDATE.md
auth-service/SAMEHOST_UPDATE_SUMMARY.md
auth-service/AuthAPIEndpoint.md
```

**Action: Move to a `docs-archive/` folder or delete if not needed**

### ❌ Development/Testing Folders

```
flowise-proxy-service-py/QuickTest/
flowise-proxy-service-py/tests-external/
flowise-proxy-service-py/tests-internal/
flowise-proxy-service-py/learn/
flowise-proxy-service-py/progress/
accounting-service/learn/
accounting-service/quickManageCredit/
accounting-service/quickManageCreditBatch/
auth-service/learn/
auth-service/examples/
auth-service/DebugTrack/
auth-service/CodeMap/
```

**Action: Optional - Can remove to reduce clutter, or keep for reference**

### ❌ Python Testing/Debug Scripts

```
flowise-proxy-service-py/check_deployment_status.py
flowise-proxy-service-py/check_migrations.py
flowise-proxy-service-py/compare_routes.py
flowise-proxy-service-py/create_test_users.py
flowise-proxy-service-py/debug_file_system.py
flowise-proxy-service-py/deploy_image_rendering.py
flowise-proxy-service-py/setup_file_system.py
flowise-proxy-service-py/test_cleanup_endpoints.py
flowise-proxy-service-py/test_collection_setup.py
flowise-proxy-service-py/test_db_connection.py
flowise-proxy-service-py/test_debug_environment.py
flowise-proxy-service-py/test_file_flow.py
flowise-proxy-service-py/test_image_rendering.py
flowise-proxy-service-py/view_chat_messages.py
accounting-service/accounting_service_test_guide.py
```

**Action: Optional - Keep if you plan to run tests, otherwise can remove**

---

## Files That Must Be Kept

### ✅ Critical Docker Files

#### All Services
```
*/Dockerfile                  - Container build instructions
*/docker-compose.yml          - Main orchestration file (keep primary one)
*/.dockerignore               - Files to exclude from build context
```

#### Flowise Proxy Service
```
flowise-proxy-service-py/init-mongo.js          - MongoDB initialization
flowise-proxy-service-py/init-mongo-prod.js     - MongoDB production setup
flowise-proxy-service-py/requirements.txt       - Python dependencies
```

#### Accounting Service
```
accounting-service/init-test-db.js              - PostgreSQL initialization
```

### ✅ Application Code
```
All files in:
  - */src/
  - */app/
  - */tests/ (if running tests)
```

### ✅ Configuration Files
```
*/package.json              - Node.js dependencies
*/tsconfig.json             - TypeScript configuration
*/jest.config.js            - Testing configuration
flowise-proxy-service-py/setup.py
```

### ✅ Windows Batch Scripts (Keep & Use These!)

#### Auth Service
```
auth-service/start_docker.bat
auth-service/rebuild_docker.bat
auth-service/rebuild_docker.ps1
auth-service/check_network.bat
```

#### Flowise Proxy Service
```
flowise-proxy-service-py/start-docker.bat
flowise-proxy-service-py/rebuild-docker.bat
flowise-proxy-service-py/rebuild-docker-test.bat
flowise-proxy-service-py/rebuild-docker-rebuild-volume.bat
flowise-proxy-service-py/setup-collections.bat
flowise-proxy-service-py/run-migrations.bat
flowise-proxy-service-py/verify-docker.bat
```

#### Accounting Service
```
accounting-service/start-docker.bat
accounting-service/rebuild-docker.bat
accounting-service/rebuild-docker-rebuild-volume.bat
accounting-service/vscodeDBDebug.bat
```

---

## Environment Configuration Plan

### Step 1: Create .env Files from Templates

#### Auth Service: Create `.env` from `.env.development`

**Location:** `auth-service/.env`

```env
# MongoDB Configuration
MONGO_URI=mongodb://mongodb-auth:27017/auth_db

# Email Configuration (MailHog for development)
EMAIL_SERVICE=smtp
EMAIL_HOST=mailhog
EMAIL_PORT=1025
EMAIL_USER=
EMAIL_PASS=
EMAIL_FROM=noreply@yourapp.com

# JWT Configuration - CRITICAL: Must match across all services!
JWT_ACCESS_SECRET=YOUR_SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS
JWT_REFRESH_SECRET=YOUR_REFRESH_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS
JWT_ACCESS_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d

# Token Expiration
VERIFICATION_CODE_EXPIRES_IN=15m
PASSWORD_RESET_EXPIRES_IN=1h

# Server Configuration
NODE_ENV=development
PORT=3000
HOST_URL=http://localhost:3000

# CORS Configuration
CORS_ORIGIN=*

# Logging
LOG_LEVEL=info
```

#### Flowise Proxy Service: Create `.env` from `.env.example`

**Location:** `flowise-proxy-service-py/.env`

```env
# JWT Configuration - MUST MATCH AUTH SERVICE!
JWT_SECRET_KEY=YOUR_SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS
JWT_ACCESS_SECRET=YOUR_SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS
JWT_REFRESH_SECRET=YOUR_REFRESH_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Flowise Configuration
FLOWISE_API_URL=https://your-flowise-endpoint.com
FLOWISE_API_KEY=your_flowise_api_key_here

# External Services URLs - Docker network names
EXTERNAL_AUTH_URL=http://auth-service:3000/api
ACCOUNTING_SERVICE_URL=http://accounting-service:3001/api

# MongoDB Database Configuration
MONGODB_URL=mongodb://admin:YOUR_MONGO_PASSWORD@mongodb-proxy:27017/flowise_proxy?authSource=admin
MONGODB_DATABASE_NAME=flowise_proxy

# Server Configuration
DEBUG=true
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000

# Collection Setup (first run)
FORCE_COLLECTION_SETUP=true
FAIL_ON_COLLECTION_SETUP_ERROR=false

# Chatflow Sync
ENABLE_CHATFLOW_SYNC=true
CHATFLOW_SYNC_INTERVAL_HOURS=0.05

# CORS
CORS_ORIGIN=*

# Streaming
MAX_STREAMING_DURATION=180000
```

#### Accounting Service: Create `.env` from `.env.example`

**Location:** `accounting-service/.env`

```env
# Server Configuration
PORT=3001
NODE_ENV=development

# PostgreSQL Database Configuration - Docker service name
DB_HOST=postgres-accounting
DB_PORT=5432
DB_NAME=accounting_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD

# JWT Configuration - MUST MATCH AUTH SERVICE!
JWT_ACCESS_SECRET=YOUR_SUPER_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS
JWT_REFRESH_SECRET=YOUR_REFRESH_SECRET_KEY_CHANGE_THIS_IN_PRODUCTION_MIN_32_CHARS

# CORS Configuration
CORS_ORIGIN=*
```

### Step 2: Generate Strong Secrets

**Use PowerShell to generate secrets:**

```powershell
# Generate a random 64-character secret
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

**Or use an online tool:**
- https://www.grc.com/passwords.htm (Perfect Passwords section)
- https://passwordsgenerator.net/ (64+ characters)

**Important:** 
- Use the SAME `JWT_ACCESS_SECRET` across all three services
- Use the SAME `JWT_REFRESH_SECRET` across all three services
- Use DIFFERENT passwords for each database

---

## Docker Deployment Strategy

### Option 1: Individual Service Deployment (Recommended for Development)

Deploy each service separately using its own docker-compose.yml:

```
auth-service/docker-compose.yml         → MongoDB + Auth Service
accounting-service/docker-compose.yml   → PostgreSQL + Accounting Service  
flowise-proxy-service-py/docker-compose.yml → MongoDB + Proxy Service
```

**Pros:**
- Easier to debug individual services
- Can restart one service without affecting others
- Better for development

**Cons:**
- Need to manage three separate docker-compose commands
- Services must connect across different Docker networks

### Option 2: Unified Docker Compose (Recommended for Production)

Create a single `docker-compose.yml` at the root that orchestrates all services.

**Pros:**
- Single command to start/stop everything
- Shared network for easy communication
- Better for production/staging

**Cons:**
- Larger stack, harder to debug
- All services start/stop together

---

## Step-by-Step Setup Guide

### Phase 1: Preparation (30 minutes)

#### 1.1 Clean Up Unnecessary Files (Optional)

```powershell
# Navigate to project root
cd C:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform

# Create backup first!
mkdir backup-$(Get-Date -Format "yyyyMMdd")
# Copy entire project to backup (optional but recommended)

# Remove Linux shell scripts (optional - they don't hurt on Windows)
# You can skip this step if you want to keep everything
```

**Recommendation:** Don't delete anything yet. Just ignore .sh files - they won't interfere.

#### 1.2 Install Prerequisites

- [ ] Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- [ ] Enable WSL 2 backend in Docker Desktop settings
- [ ] Allocate resources in Docker Desktop:
  - Memory: 8GB minimum
  - CPUs: 4 cores minimum
  - Swap: 2GB
  - Disk image size: 100GB

#### 1.3 Verify Docker Installation

```powershell
# Check Docker version
docker --version
# Should show: Docker version 24.x.x or higher

# Check Docker Compose
docker compose version
# Should show: Docker Compose version v2.x.x

# Verify Docker is running
docker ps
# Should show empty list or running containers
```

### Phase 2: Environment Configuration (45 minutes)

#### 2.1 Generate Secrets

```powershell
# Generate JWT Access Secret
$jwt_access_secret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host "JWT_ACCESS_SECRET=$jwt_access_secret"

# Generate JWT Refresh Secret  
$jwt_refresh_secret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})
Write-Host "JWT_REFRESH_SECRET=$jwt_refresh_secret"

# Generate MongoDB Password
$mongo_password = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "MONGO_PASSWORD=$mongo_password"

# Generate PostgreSQL Password
$postgres_password = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "POSTGRES_PASSWORD=$postgres_password"
```

**Save these values in a secure location (e.g., password manager)**

#### 2.2 Create Auth Service .env

```powershell
cd auth-service

# Copy template
Copy-Item .env.development .env

# Edit .env file with your favorite editor
notepad .env
# Or: code .env (if using VS Code)
```

**Edit the following values:**
- `MONGO_URI=mongodb://mongodb-auth:27017/auth_db`
- `JWT_ACCESS_SECRET=` (paste your generated secret)
- `JWT_REFRESH_SECRET=` (paste your generated secret)
- `NODE_ENV=development`

#### 2.3 Create Flowise Proxy Service .env

```powershell
cd ..\flowise-proxy-service-py

# Copy template
Copy-Item .env.example .env

# Edit .env file
notepad .env
```

**Edit the following values:**
- `JWT_ACCESS_SECRET=` (SAME as auth service!)
- `JWT_REFRESH_SECRET=` (SAME as auth service!)
- `FLOWISE_API_URL=` (your Flowise endpoint)
- `FLOWISE_API_KEY=` (your Flowise API key)
- `MONGODB_URL=mongodb://admin:YOUR_MONGO_PASSWORD@mongodb-proxy:27017/flowise_proxy?authSource=admin`
- Replace `YOUR_MONGO_PASSWORD` with generated password
- `EXTERNAL_AUTH_URL=http://auth-service:3000/api`
- `ACCOUNTING_SERVICE_URL=http://accounting-service:3001/api`

#### 2.4 Create Accounting Service .env

```powershell
cd ..\accounting-service

# Copy template
Copy-Item .env.example .env

# Edit .env file
notepad .env
```

**Edit the following values:**
- `JWT_ACCESS_SECRET=` (SAME as auth service!)
- `JWT_REFRESH_SECRET=` (SAME as auth service!)
- `DB_HOST=postgres-accounting`
- `DB_PASSWORD=` (paste your generated PostgreSQL password)

### Phase 3: Docker Network Setup (15 minutes)

#### 3.1 Create Shared Docker Network

```powershell
# Create a shared network for all services
docker network create chatproxy-network
```

#### 3.2 Update Docker Compose Files

You'll need to update each service's docker-compose.yml to use the shared network.

**For each service, add to docker-compose.yml:**

```yaml
networks:
  default:
    external: true
    name: chatproxy-network
```

### Phase 4: Build and Deploy Services (30 minutes)

#### 4.1 Deploy Auth Service

```powershell
cd C:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\auth-service

# Build and start
docker compose up -d --build

# Check logs
docker compose logs -f

# Wait for "Server running" message
# Press Ctrl+C to exit logs
```

#### 4.2 Deploy Accounting Service

```powershell
cd ..\accounting-service

# Build and start
docker compose up -d --build

# Check logs
docker compose logs -f

# Wait for "Database synced" message
```

#### 4.3 Deploy Flowise Proxy Service

```powershell
cd ..\flowise-proxy-service-py

# Build and start
docker compose up -d --build

# Check logs
docker compose logs -f

# Wait for "Application startup complete" message
```

### Phase 5: Verification (20 minutes)

#### 5.1 Check All Containers

```powershell
# List all running containers
docker ps

# You should see:
# - auth-service (port 3000)
# - accounting-service (port 3001)
# - flowise-proxy (port 8000)
# - mongodb-auth (port 27017)
# - mongodb-proxy (port 27017 internal)
# - postgres-accounting (port 5432)
```

#### 5.2 Test Health Endpoints

```powershell
# Test Auth Service
Invoke-WebRequest http://localhost:3000/health

# Test Accounting Service
Invoke-WebRequest http://localhost:3001/api/health

# Test Flowise Proxy Service
Invoke-WebRequest http://localhost:8000/health
```

**Expected response for each: `{"status":"ok"}`**

#### 5.3 Create Test Admin User

```powershell
cd auth-service

# Use the provided batch script or PowerShell
# Check if quickCreateAdminPy folder has a Windows script

# Or use curl/Invoke-WebRequest to create user via API
```

### Phase 6: Configure Flowise API Connection (15 minutes)

#### 6.1 Update Flowise Proxy .env

Ensure your `.env` in flowise-proxy-service-py has:
- Valid `FLOWISE_API_URL`
- Valid `FLOWISE_API_KEY`

#### 6.2 Restart Flowise Proxy

```powershell
cd flowise-proxy-service-py
docker compose restart
```

---

## Verification Checklist

### ✅ Pre-Deployment Checklist

- [ ] Docker Desktop installed and running
- [ ] WSL 2 enabled
- [ ] At least 8GB RAM allocated to Docker
- [ ] All three `.env` files created
- [ ] JWT secrets are IDENTICAL across all services
- [ ] Database passwords are UNIQUE and strong
- [ ] Flowise API URL and key configured

### ✅ Deployment Checklist

- [ ] Docker network `chatproxy-network` created
- [ ] Auth service container running
- [ ] Auth service MongoDB container running
- [ ] Accounting service container running
- [ ] Accounting service PostgreSQL container running
- [ ] Flowise proxy service container running
- [ ] Flowise proxy MongoDB container running

### ✅ Health Check Checklist

- [ ] Auth service health endpoint responds (http://localhost:3000/health)
- [ ] Accounting service health endpoint responds (http://localhost:3001/api/health)
- [ ] Flowise proxy health endpoint responds (http://localhost:8000/health)
- [ ] No error messages in any service logs

### ✅ Functional Testing Checklist

- [ ] Can create a user via Auth service API
- [ ] Can login and receive JWT token
- [ ] Can allocate credits via Accounting service API
- [ ] Can check credit balance
- [ ] Can send chat request through Flowise proxy
- [ ] Chat response received successfully
- [ ] Credits deducted correctly

---

## Common Issues & Solutions

### Issue 1: Port Already in Use

**Error:** "Bind for 0.0.0.0:3000 failed: port is already allocated"

**Solution:**
```powershell
# Find what's using the port
netstat -ano | findstr :3000

# Kill the process
taskkill /PID <PID_NUMBER> /F

# Or change the port in docker-compose.yml:
# ports:
#   - "3001:3000"  # External:Internal
```

### Issue 2: JWT Verification Failed

**Error:** "Invalid token" or "Token verification failed"

**Solution:**
- Verify `JWT_ACCESS_SECRET` is IDENTICAL in all three `.env` files
- Check for extra spaces or line breaks in the secret
- Restart all services after changing secrets

### Issue 3: Cannot Connect to Database

**Error:** "Cannot connect to MongoDB/PostgreSQL"

**Solution:**
- Verify container names match `.env` configuration
- Check containers are on same Docker network
- Wait 30 seconds for databases to initialize
- Check database logs: `docker compose logs mongodb-auth`

### Issue 4: Service Cannot Communicate

**Error:** "Cannot connect to auth-service" or "Connection refused"

**Solution:**
- Verify all services use the same Docker network
- Use container names (not localhost) in `.env` URLs
- Example: `EXTERNAL_AUTH_URL=http://auth-service:3000/api`
- NOT: `EXTERNAL_AUTH_URL=http://localhost:3000/api`

---

## Maintenance Commands

### View Logs
```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f auth-service

# Last 100 lines
docker compose logs --tail=100 auth-service
```

### Restart Services
```powershell
# Restart specific service
docker compose restart auth-service

# Restart all services
docker compose restart
```

### Stop Services
```powershell
# Stop all services
docker compose down

# Stop and remove volumes (DELETES DATA!)
docker compose down -v
```

### Update Code
```powershell
# Pull latest code
git pull

# Rebuild containers
cd auth-service
docker compose up -d --build

cd ..\accounting-service
docker compose up -d --build

cd ..\flowise-proxy-service-py
docker compose up -d --build
```

### Database Backup
```powershell
# Backup MongoDB
docker exec mongodb-auth mongodump --out /backup

# Backup PostgreSQL
docker exec postgres-accounting pg_dump -U postgres accounting_db > backup.sql
```

---

## Production Deployment Considerations

### Security Hardening

1. **Change all default passwords**
2. **Use strong JWT secrets (64+ characters)**
3. **Enable HTTPS/TLS**
4. **Restrict CORS_ORIGIN** to your domain
5. **Enable rate limiting**
6. **Set NODE_ENV=production**
7. **Disable debug logging**
8. **Use environment-specific .env files**

### Scaling

1. **Add Docker Compose resource limits**
2. **Use Docker Swarm or Kubernetes for orchestration**
3. **Set up load balancer**
4. **Enable database replication**
5. **Implement caching (Redis)**
6. **Set up monitoring (Prometheus/Grafana)**

### Monitoring

1. **Set up health check endpoints monitoring**
2. **Configure log aggregation**
3. **Set up alerts for service failures**
4. **Monitor resource usage**
5. **Track API response times**

---

## Next Steps

After successful deployment:

1. **Create admin user** for system management
2. **Allocate credits** to users via admin API
3. **Configure Flowise** chatflows
4. **Test end-to-end chat flow**
5. **Set up monitoring and logging**
6. **Configure backups**
7. **Document custom configurations**

---

## Support & Resources

### Documentation
- [SERVICE_ARCHITECTURE.md](./SERVICE_ARCHITECTURE.md) - System architecture overview
- [auth-service/README.md](./auth-service/README.md) - Auth service documentation
- [accounting-service/docs/](./accounting-service/docs/) - Accounting service API docs
- [flowise-proxy-service-py/README.md](./flowise-proxy-service-py/README.md) - Proxy service docs

### Docker Commands Reference
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)

### Troubleshooting
- Check service logs: `docker compose logs -f`
- Verify network: `docker network ls`
- Check containers: `docker ps -a`
- Inspect container: `docker inspect <container_name>`

---

## Summary

This deployment plan provides a complete guide for setting up the three-service architecture on Windows using Docker. Key points:

- **Remove:** Linux shell scripts (.sh files) - optional, they don't interfere
- **Keep:** All .bat files, Dockerfiles, docker-compose.yml files, application code
- **Create:** Three .env files from templates with matching JWT secrets
- **Deploy:** Use docker-compose to orchestrate all services
- **Verify:** Test health endpoints and end-to-end functionality

Estimated total setup time: **2-3 hours** for first-time deployment.
