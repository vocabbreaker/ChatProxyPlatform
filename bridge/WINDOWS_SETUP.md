# Bridge UI - Windows Docker Setup

React + TypeScript + Vite frontend for ChatProxy Platform.

---

## Quick Start (Windows Docker)

### Prerequisites
- Docker Desktop installed and running
- No other service using port 3082

### Start Bridge UI

```batch
start.bat
```

**Access:** http://localhost:3082

---

## Management Commands

| Command | Purpose |
|---------|---------|
| `start.bat` | Build and start Docker container |
| `stop.bat` | Stop and remove container |
| `rebuild.bat` | Full rebuild after code changes |
| `logs.bat` | View container logs (real-time) |

---

## Configuration

The Bridge UI connects to the Flowise Proxy API. Configure the API URL in `docker-compose.yml`:

```yaml
environment:
  - VITE_FLOWISE_PROXY_API_URL=${FLOWISE_PROXY_URL:-http://host.docker.internal:8000}
```

**Default:** `http://host.docker.internal:8000` (local Flowise Proxy)

**To change:**
1. Edit `docker-compose.yml` and change the default URL, OR
2. Set environment variable before starting:
   ```batch
   set FLOWISE_PROXY_URL=https://your-api-domain.com
   start.bat
   ```

---

## Architecture

**Bridge UI** is the React frontend that:
- Provides chat interface for users
- Handles authentication with Auth Service
- Communicates with Flowise Proxy API
- Renders AI responses with math/markdown support
- Manages file uploads and chat sessions

**Tech Stack:**
- React 18 + TypeScript
- Vite (build tool)
- Zustand (state management)
- TailwindCSS (styling)
- MathJax (math rendering)
- i18next (internationalization)

---

## Service Endpoints

| Service | Port | Purpose |
|---------|------|---------|
| **Bridge UI** | 3082 | React frontend (this service) |
| Flowise Proxy | 8000 | Python API backend |
| Auth Service | 3000 | User authentication |
| Flowise | 3002 | AI flow builder |

---

## Docker Commands

### Check Status
```batch
docker ps | findstr bridge-ui
```

### View Logs
```batch
docker compose logs -f bridge-ui
```

### Stop Container
```batch
docker compose down
```

### Rebuild After Code Changes
```batch
rebuild.bat
```

### Force Clean Rebuild
```batch
docker compose down
docker system prune -f
docker compose up -d --build --force-recreate
```

---

## Development

For local development (without Docker):

```batch
npm install
npm run dev
```

**Note:** Local development requires `.env` file with `VITE_FLOWISE_PROXY_API_URL`

---

## Troubleshooting

### Port 3082 Already in Use
```batch
netstat -ano | findstr :3082
taskkill /PID <PID> /F
```

### Container Won't Start
1. Check Docker Desktop is running
2. View logs: `logs.bat`
3. Try rebuild: `rebuild.bat`

### Cannot Connect to API
1. Verify Flowise Proxy is running on port 8000
2. Check `docker-compose.yml` has correct API URL
3. Test API: `curl http://localhost:8000/health`

### White Screen / Build Errors
1. Stop container: `stop.bat`
2. Clean rebuild: `rebuild.bat`
3. Check logs: `logs.bat`

---

## Files Structure

```
bridge/
├── start.bat              # Start Docker container
├── stop.bat               # Stop Docker container
├── rebuild.bat            # Rebuild Docker container
├── logs.bat               # View container logs
├── docker-compose.yml     # Docker configuration
├── Dockerfile             # Container build instructions
├── nginx.conf             # Nginx web server config
├── .env.example           # Configuration reference
├── package.json           # Node.js dependencies
├── vite.config.ts         # Vite build configuration
├── tsconfig.json          # TypeScript configuration
└── src/                   # React source code
    ├── components/        # React components
    ├── pages/             # Page components
    ├── api/               # API client functions
    ├── store/             # Zustand state stores
    ├── utils/             # Utility functions
    └── locales/           # i18n translations
```

---

## Production Deployment

1. Update API URL in `docker-compose.yml`:
   ```yaml
   - VITE_FLOWISE_PROXY_API_URL=https://your-production-api.com
   ```

2. Build and start:
   ```batch
   start.bat
   ```

3. Verify health:
   ```batch
   curl http://localhost:3082
   ```

---

## Support

For issues:
1. Check logs: `logs.bat`
2. Verify Docker Desktop is running
3. Check other services are running (Auth, Flowise Proxy)
4. Try rebuild: `rebuild.bat`
