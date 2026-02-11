# Flowise Proxy Service

Python FastAPI proxy service for Flowise with authentication, credit management, and chat history.

---

## Quick Start (Windows Docker)

### Start the Service

```batch
start.bat
```

Access at: **http://localhost:8000**

### Other Commands

```batch
stop.bat         # Stop containers
rebuild.bat      # Rebuild after code changes  
logs.bat         # View real-time logs
start-docker.bat # Alternative start command
```

---

## Configuration

Edit `.env` file before starting:

```env
# Flowise Configuration
FLOWISE_API_URL=http://flowise:3002
FLOWISE_API_KEY=

# External Services (Docker network)
EXTERNAL_AUTH_URL=http://auth-service:3000
ACCOUNTING_SERVICE_URL=http://accounting-service:3001

# MongoDB
MONGODB_URL=mongodb://admin:password@mongodb-proxy:27017/flowise_proxy?authSource=admin
MONGODB_DATABASE_NAME=flowise_proxy
```

---

## Architecture

```
Bridge UI (3082) → Flowise Proxy (8000) → Flowise (3002)
                           ↓
                    Auth Service (3000)
                           ↓
                 Accounting Service (3001)
```

---

## API Endpoints

### Authentication
- `POST /api/v1/chat/authenticate` - Login
- `POST /api/v1/chat/refresh` - Refresh token

### Chat
- `POST /api/v1/chat/predict/stream/store` - Send message
- `GET /api/v1/chat/sessions` - Get sessions
- `GET /api/v1/chat/sessions/{id}/history` - Get history

### Admin
- `POST /api/v1/admin/chatflows/sync` - Sync chatflows
- `GET /api/v1/admin/chatflows` - List chatflows
- `POST /api/v1/admin/chatflows/{id}/users` - Assign user to chatflow

---

## Troubleshooting

**Can't connect to Flowise:**
- Check `FLOWISE_API_URL` in `.env`
- Ensure Flowise container is running: `docker ps`

**Authentication fails:**
- Verify auth-service is running
- Check `EXTERNAL_AUTH_URL` points to `http://auth-service:3000`

**View Logs:**
```batch
logs.bat
```

---

## Requirements

- Docker Desktop for Windows
- All services on `chatproxy-network`

---

For more information, see [WINDOWS_DOCKER_ENDPOINTS.md](../WINDOWS_DOCKER_ENDPOINTS.md) in the root folder.
