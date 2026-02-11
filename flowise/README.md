# Flowise Docker Setup

This directory contains the Docker setup for deploying [Flowise](https://github.com/FlowiseAI/Flowise) - an open-source UI visual tool to build customized LLM flows.

## � Database Configuration

**Current Setup: PostgreSQL** (switched from SQLite for production use)

### Why PostgreSQL?
- ✅ Better performance for production workloads
- ✅ More reliable for concurrent users  
- ✅ Easier to backup and restore
- ✅ Better data integrity and ACID compliance
- ✅ Supports advanced features (full-text search, JSON queries, etc.)

### Database Details:
- **Type:** PostgreSQL 15
- **Container:** `flowise-postgres`
- **Database Name:** `flowise`
- **User:** `flowiseuser`
- **Password:** `flowisepass`
- **Internal Port:** 5432
- **External Port:** 5433 (accessible from host)

---

## 🚀 Quick Start

### Start Flowise with PostgreSQL

```bash
cd flowise
start.bat
```

Or manually:
```bash
docker compose up -d
```

Access Flowise at: http://localhost:3002

### Stop Flowise

```bash
stop.bat
```

Or manually:
```bash
docker compose down
```

---

## 🗄️ Database Management

### Connect to PostgreSQL

From host machine:
```bash
psql -h localhost -p 5433 -U flowiseuser -d flowise
```

From Docker:
```bash
docker exec -it flowise-postgres psql -U flowiseuser -d flowise
```

### Backup Database

```bash
docker exec flowise-postgres pg_dump -U flowiseuser flowise > flowise_backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
docker exec -i flowise-postgres psql -U flowiseuser -d flowise < flowise_backup.sql
```

### View Tables

```bash
docker exec -it flowise-postgres psql -U flowiseuser -d flowise -c "\dt"
```

---

### 4. Stop and Remove Data

```bash
docker compose down -v
```

---

## 📋 Configuration

### Environment Variables

Copy `.env` file and adjust values:

```bash
cp .env .env.local
# Edit .env with your preferred settings
```

Key configurations:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Flowise web interface port |
| `DATABASE_TYPE` | sqlite | Database type (sqlite, postgres, mysql) |
| `FLOWISE_USERNAME` | - | Optional: Basic auth username |
| `FLOWISE_PASSWORD` | - | Optional: Basic auth password |
| `DISABLE_FLOWISE_TELEMETRY` | true | Disable telemetry |

### Using PostgreSQL

1. Uncomment PostgreSQL configuration in `.env`:
   ```env
   DATABASE_TYPE=postgres
   DATABASE_HOST=flowise-postgres
   DATABASE_PORT=5432
   DATABASE_NAME=flowise
   DATABASE_USER=flowiseuser
   DATABASE_PASSWORD=flowisepass
   ```

2. Start with postgres profile:
   ```bash
   docker compose --profile postgres up -d
   ```

---

## 🔗 Integration with ChatProxy Platform

Flowise is connected to the `chatproxy-network` and can be accessed by other services:

### From Flowise Proxy Service

The flowise-proxy-service-py can call Flowise APIs:

```python
# In flowise-proxy-service-py
FLOWISE_API_BASE_URL=http://flowise:3000/api/v1
```

### Network Architecture

```
┌─────────────────────────────────────────────┐
│        ChatProxy Platform Network           │
│                                             │
│  ┌──────────────┐    ┌─────────────────┐  │
│  │ Auth Service │    │ Accounting Svc  │  │
│  │ Port: 3000   │    │ Port: 3001      │  │
│  └──────────────┘    └─────────────────┘  │
│                                             │
│  ┌──────────────┐    ┌─────────────────┐  │
│  │ Flowise Proxy│───►│  Flowise        │  │
│  │ Port: 8000   │    │  Port: 3000     │  │
│  └──────────────┘    └─────────────────┘  │
│                           │                 │
│                           ▼                 │
│                      AI Models              │
└─────────────────────────────────────────────┘
```

---

## 📚 Flowise API Endpoints

### Key API Endpoints

1. **Create Prediction (Chat)**
   ```http
   POST /api/v1/prediction/{chatflowId}
   Content-Type: application/json

   {
     "question": "Hello, how are you?",
     "overrideConfig": {},
     "chatId": "optional-chat-id"
   }
   ```

2. **List Chatflows**
   ```http
   GET /api/v1/chatflows
   ```

3. **Get Chatflow Details**
   ```http
   GET /api/v1/chatflows/{id}
   ```

4. **Upload File**
   ```http
   POST /api/v1/vector/upsert/{chatflowId}
   Content-Type: multipart/form-data
   ```

### API Authentication

If you set `FLOWISE_USERNAME` and `FLOWISE_PASSWORD`, add Basic Auth headers:

```bash
Authorization: Basic <base64(username:password)>
```

Or use API keys (configured in Flowise UI under Settings > API Keys).

---

## 🛠️ Management Commands

### View Logs

```bash
# Flowise logs
docker logs flowise -f

# PostgreSQL logs (if using postgres profile)
docker logs flowise-postgres -f
```

### Restart Service

```bash
docker compose restart flowise
```

### Update Flowise

```bash
docker compose pull
docker compose up -d
```

### Backup Data

```bash
# Backup SQLite database
docker cp flowise:/root/.flowise ./flowise-backup

# Backup PostgreSQL
docker exec flowise-postgres pg_dump -U flowiseuser flowise > flowise-backup.sql
```

### Restore Data

```bash
# Restore SQLite
docker cp ./flowise-backup flowise:/root/.flowise

# Restore PostgreSQL
docker exec -i flowise-postgres psql -U flowiseuser flowise < flowise-backup.sql
```

---

## 🔧 Advanced Configuration

### S3 Storage

To use AWS S3 for file storage:

```env
STORAGE_TYPE=s3
S3_STORAGE_BUCKET_NAME=your-bucket
S3_STORAGE_ACCESS_KEY_ID=your-access-key
S3_STORAGE_SECRET_ACCESS_KEY=your-secret-key
S3_STORAGE_REGION=us-east-1
```

### Redis for Queuing

For production deployments with queue support:

```env
MODE=queue
REDIS_URL=redis://your-redis-host:6379
```

### Custom Models Configuration

Create a `models.json` file and mount it:

```yaml
volumes:
  - ./models.json:/root/.flowise/models.json
```

Then set:
```env
MODEL_LIST_CONFIG_JSON=/root/.flowise/models.json
```

---

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:3000/api/v1/ping
```

Response:
```json
{"message":"pong"}
```

### Container Status

```bash
docker compose ps
```

### Resource Usage

```bash
docker stats flowise
```

---

## 🐛 Troubleshooting

### Port Already in Use

If port 3000 is taken, change it in `.env`:

```env
PORT=3005
```

### Permission Issues

If you encounter permission errors:

```bash
docker compose down -v
docker volume rm flowise_flowise_data
docker compose up -d
```

### Database Connection Issues

Check PostgreSQL logs:
```bash
docker logs flowise-postgres
```

Ensure database credentials match in both services.

### Cannot Access UI

1. Check if container is running:
   ```bash
   docker ps | grep flowise
   ```

2. Check logs:
   ```bash
   docker logs flowise --tail 100
   ```

3. Verify network:
   ```bash
   docker network inspect chatproxy-network
   ```

---

## 📖 Additional Resources

- [Flowise Official Documentation](https://docs.flowiseai.com/)
- [Flowise GitHub Repository](https://github.com/FlowiseAI/Flowise)
- [Flowise Discord Community](https://discord.gg/jbaHfsRVBW)
- [API Documentation](http://localhost:3000/api-docs) (when Flowise is running)

---

## 🔐 Security Notes

⚠️ **Important Security Considerations:**

1. **Change Default Passwords**: Always change default passwords in production
2. **Enable Authentication**: Set `FLOWISE_USERNAME` and `FLOWISE_PASSWORD`
3. **Use HTTPS**: Configure a reverse proxy (nginx/traefik) with SSL
4. **Restrict CORS**: Set specific origins instead of `*` in production
5. **Network Isolation**: Use Docker networks to isolate services
6. **Regular Updates**: Keep Flowise image updated for security patches

### Production Deployment Checklist

- [ ] Set strong authentication credentials
- [ ] Configure PostgreSQL instead of SQLite
- [ ] Enable HTTPS with SSL certificates
- [ ] Set specific CORS origins
- [ ] Configure S3 or cloud storage for files
- [ ] Set up Redis for queue management
- [ ] Enable proper logging and monitoring
- [ ] Configure regular backups
- [ ] Implement rate limiting (via reverse proxy)
- [ ] Review and restrict network access

---

## 📝 License

Flowise is licensed under Apache License 2.0. See [Flowise LICENSE](https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md) for details.
