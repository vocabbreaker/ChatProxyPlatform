# Windows Docker Deployment - Complete Setup Guide

Complete step-by-step guide to deploy the ChatProxy Platform on Windows using Docker.

---

## 🚀 Quick Start

**For fresh Windows installations (no prior setup):**
1. Read the complete **[DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md)** - step-by-step guide for beginners
2. Track your progress with **[DEPLOYMENT_PROGRESS.md](DEPLOYMENT_PROGRESS.md)** - printable checklist
3. Run **`check_system.bat`** - automated system checker for prerequisites

**For existing installations:**
Continue with this guide below.

---

## Prerequisites

- Docker Desktop installed and running
- Git (for cloning the repository)
- Python 3.x installed
- Windows PowerShell or Command Prompt

**Quick Check:** Run `check_system.bat` to verify all prerequisites are met.

---

## Step 1: Launch Flowise with PostgreSQL

### 1.1 Start Flowise Docker Container

```batch
cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\flowise
start-with-postgres.bat
```

**Wait for containers to start** (check status: `docker ps`)

### 1.2 Access Flowise Web Interface

Open your browser and navigate to:
```
http://localhost:3002
```

**Note:** Flowise now uses **PostgreSQL** instead of SQLite for better performance and reliability.

### 1.3 Setup Flowise Admin Account

On first access, Flowise will prompt you to create an admin account:

- **Name:** `admin`
- **Email:** `ecysit@eduhk.hk`
- **Password:** `Admin@2026`

**Important:** Complete the initial setup wizard and save your credentials.

### 1.4 Generate Flowise API Key

The Flowise Proxy Service requires an API key to sync chatflows from Flowise.

1. **Login to Flowise:**
   - Open http://localhost:3002
   - Login with your admin credentials (ecysit@eduhk.hk / Admin@2026)

2. **Generate API Key:**
   - Click on your profile icon (top-right corner)
   - Navigate to **Settings** → **API Keys**
   - Click **Add New Key** or **Generate API Key**
   - Copy the generated API key (e.g., `A27MfYLThKBwYcpDb2M9s6rwXIwUAly9P8j_ujX_J9I`)

3. **Configure Flowise Proxy:**
   - Open the Flowise Proxy `.env` file:
     ```batch
     cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\flowise-proxy-service-py
     notepad .env
     ```
   - Find the line: `FLOWISE_API_KEY=`
   - Paste your API key: `FLOWISE_API_KEY=A27MfYLThKBwYcpDb2M9s6rwXIwUAly9P8j_ujX_J9I`
   - Save and close the file

4. **Restart Flowise Proxy** (if already running):
   ```batch
   cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\flowise-proxy-service-py
   docker compose restart
   ```

**Note:** Without the API key, chatflow synchronization will fail with "401 Unauthorized" errors.

---

## Step 2: Launch Auth Service

### 2.1 Start Auth Service Containers

```batch
cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\auth-service
start.bat
```

**Services Started:**
- Auth Service: `http://localhost:3000`
- MongoDB: `localhost:27017`
- MailHog UI: `http://localhost:8025`

### 2.2 Create Admin Account

```batch
cd quickCreateAdminPy
setup_and_run.bat
```

**Default Admin Credentials:**
- **Username:** `admin`
- **Email:** `admin@example.com`
- **Password:** `admin@admin`

### 2.3 Verify Admin Account

After the script completes, verify the admin account was created successfully by checking the output or running:

```batch
list_users.bat
```

---

## Step 3: Manage Users and Credits (CSV-Based System)

### 3.1 Overview

The platform includes a simple CSV-based system for managing users and credits - perfect for teachers without computer knowledge!

**What you can do:**
- Create new teacher and student accounts
- Remove existing users
- Set and update credit amounts
- All from a simple spreadsheet (Excel/Notepad)

### 3.2 Edit Users in CSV

Navigate to the user management folder:
```batch
cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\auth-service\quickCreateAdminPy
```

Open `users.csv` in Excel or Notepad and edit:

| action | username  | email              | password   | role    | fullName      | credits |
|--------|-----------|-------------------|------------|---------|---------------|---------|
| create | teacher1  | teacher1@school.com| Teacher1!  | teacher | Teacher One   | 5000    |
| create | student1  | student1@school.com| Student1!  | student | Student One   | 1000    |

**Column Guide:**
- **action:** `create` (add user) or `delete` (remove user)
- **username:** Unique username for login
- **email:** User's email address (must be unique)
- **password:** Strong password (8+ characters, letters + numbers)
- **role:** `teacher` (more credits) or `student` (standard user)
- **fullName:** Display name
- **credits:** Amount of AI credits (e.g., 5000 for teachers, 1000 for students)

### 3.3 Apply Changes - One-Click Sync

After editing `users.csv`, simply run:

```batch
sync_all_users.bat
```

**What this does automatically:**
1. Creates new users (action=create)
2. Deletes users (action=delete)
3. Verifies all users (enables login)
4. Initializes users in accounting system
5. Sets/updates credits for all users

**Wait for:** `SUCCESS! All users and credits synchronized`

### 3.4 Common Tasks

#### Add a New Student
1. Open `users.csv` in Excel
2. Add a row: `create,student6,student6@school.com,Student6!,student,John Smith,1000`
3. Save file
4. Run `sync_all_users.bat`

#### Add a New Teacher
1. Open `users.csv` in Excel
2. Add a row: `create,teacher4,teacher4@school.com,Teacher4!,teacher,Jane Doe,5000`
3. Save file
4. Run `sync_all_users.bat`

#### Remove a User
1. Open `users.csv` in Excel
2. Change `create` to `delete` for that user's row
3. Save file
4. Run `sync_all_users.bat`

#### Update Credits
1. Open `users.csv` in Excel
2. Change the number in the `credits` column
3. Save file
4. Run `sync_all_users.bat`

### 3.5 Detailed Instructions

For complete step-by-step instructions designed for non-technical users, see:
```
auth-service\quickCreateAdminPy\TEACHER_GUIDE.md
```

---

## Service Endpoints Summary

| Service | Endpoint | Purpose |
|---------|----------|---------|
| **Flowise** | http://localhost:3002 | AI Flow Builder |
| **Auth Service** | http://localhost:3000 | Authentication API |
| **MailHog UI** | http://localhost:8025 | Email Testing |
| **MongoDB** | localhost:27017 | Auth Database |
| **PostgreSQL** | localhost:5433 | Flowise Database |

---

## Admin Credentials

### Flowise Admin
- **Name:** `admin`
- **Email:** `ecysit@eduhk.hk`
- **Password:** `Admin@2026`
- **Access:** http://localhost:3002
- **API Key:** `A27MfYLThKBwYcpDb2M9s6rwXIwUAly9P8j_ujX_J9I` (configured in flowise-proxy-service-py/.env)

### Auth Service Admin
- **Username:** `admin`
- **Email:** `admin@example.com`
- **Password:** `admin@admin`
- **API:** http://localhost:3000

---

## Next Steps

1. **Manage Users and Credits:**
   ```batch
   cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\auth-service\quickCreateAdminPy
   notepad users.csv              # Edit users
   sync_all_users.bat             # Apply changes
   ```

2. **Test Authentication:**
   ```batch
   cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\auth-service\quickCreateAdminPy
   test_login.bat
   ```

3. **Create Flowise Flow:**
   - Log in to Flowise at http://localhost:3002
   - Create your first chatflow
   - Configure integrations

4. **Launch Additional Services** (if needed):
   - Flowise Proxy Service
   - Accounting Service

5. **Initialize Admin User in Flowise Proxy** (One-time setup):
   ```batch
   cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\flowise-proxy-service-py
   docker exec flowise-proxy python /tmp/sync_admin_chatflows.py
   ```
   
   **This script will automatically:**
   - Create admin user in flowise-proxy database
   - Assign all chatflows from Flowise to admin
   - Allocate 5000 credits to admin in accounting service
   
   **Expected output:**
   ```
   ✅ SETUP COMPLETE!
      User: admin
      Chatflows: 1
      Credits: 5000
   ```

---

## Troubleshooting

### Flowise won't start
- Check port 3002 is not in use: `netstat -ano | findstr :3002`
- View logs: `docker logs flowise -f`

### Auth Service won't start
- Check port 3000 is not in use: `netstat -ano | findstr :3000`
- View logs: `cd auth-service && logs.bat`

### Admin account not created
- Check MongoDB is running: `docker ps | findstr mongodb-auth`
- Manually verify in MongoDB:
  ```batch
  docker exec -i mongodb-auth mongosh auth_db --eval "db.users.find()"
  ```

---

## Management Commands

### Flowise
```batch
cd flowise
start-with-postgres.bat    # Start
stop.bat                   # Stop
```

### Auth Service
```batch
cd auth-service
start.bat                  # Start
stop.bat                   # Stop
rebuild.bat                # Rebuild after changes
logs.bat                   # View logs
```

### User Management
```batch
cd auth-service\quickCreateAdminPy
notepad users.csv          # Edit users/credits
sync_all_users.bat         # Apply all changes
```

---

## Security Notes

⚠️ **IMPORTANT:** The default credentials provided here are for **development only**. 

Before deploying to production:
1. Change all default passwords
2. Update JWT secrets in `.env`
3. Configure proper CORS origins
4. Enable HTTPS
5. Set up proper database backups

---

## Support

For issues or questions, check:
- Service logs using `logs.bat` in each service directory
- Docker container status: `docker ps -a`
- Network connectivity: `docker network ls`
