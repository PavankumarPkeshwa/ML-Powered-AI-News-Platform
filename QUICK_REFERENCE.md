# 🚀 Quick Reference Guide

## Start Everything

```bash
# One command to start all services
./start-all.sh
```

## Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | User Interface |
| Backend | http://localhost:5000 | API Gateway |
| GenAI | http://localhost:8000 | AI Service |

## Essential Commands

### Ingest News Articles

```bash
# Using Python script (recommended)
python3 ingest-news.py

# Single URL
curl "http://localhost:8000/agent/ingest?url=https://example.com/article"

# Batch scraping
curl "http://localhost:8000/scraper/cron"
```

### Stop Services

```bash
# If using start-all.sh
Ctrl+C

# Or manually kill processes
lsof -ti:8000 | xargs kill -9  # GenAI
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

### View Logs

```bash
# Real-time logs
tail -f logs/genai.log
tail -f logs/backend.log
tail -f logs/frontend.log
```

## Common Tasks

### Test GenAI Service

```bash
# Health check
curl http://localhost:8000/

# Get news articles
curl "http://localhost:8000/news/fetch?limit=5"

# Search articles
curl "http://localhost:8000/news/search?q=technology"

# Chat with AI
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the latest news?"}'
```

### Test Backend API

```bash
# Health check
curl http://localhost:5000/

# Get articles
curl http://localhost:5000/api/articles

# Get featured article
curl http://localhost:5000/api/featured

# Search
curl "http://localhost:5000/api/search?q=AI"

# Chat
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about tech news"}'
```

## Troubleshooting

### Problem: No articles in UI

**Solution:**
```bash
# 1. Check if GenAI service is running
curl http://localhost:8000/

# 2. Ingest some articles
python3 ingest-news.py

# 3. Verify articles are in VectorDB
curl http://localhost:8000/news/fetch
```

### Problem: Chatbot not responding

**Solution:**
```bash
# 1. Check chatbot health
curl http://localhost:8000/chat/health

# 2. Make sure VectorDB has articles
curl "http://localhost:8000/news/fetch?limit=1"

# 3. Check GenAI logs
tail -f logs/genai.log
```

### Problem: Backend can't connect to GenAI

**Solution:**
```bash
# 1. Verify GenAI is running
curl http://localhost:8000/

# 2. Check Backend .env file
cat Backend/.env
# Should have: GENAI_SERVICE_URL=http://localhost:8000

# 3. Restart Backend
cd Backend && npm run dev
```

### Problem: Port already in use

**Solution:**
```bash
# Find and kill process on port
lsof -ti:8000 | xargs kill -9

# Or change port in respective config
```

## Development Workflow

### 1. Start Services
```bash
./start-all.sh
```

### 2. Populate Data
```bash
python3 ingest-news.py
```

### 3. Open Application
```bash
# Open in browser
http://localhost:5173
```

### 4. Develop
- Frontend: Auto-reloads on file changes
- Backend: Using nodemon for auto-reload
- GenAI: Using uvicorn --reload

### 5. View Changes
- Frontend changes reflect immediately
- Backend changes auto-reload
- GenAI changes auto-reload

## API Quick Reference

### GenAI Service (Port 8000)

```bash
# News Endpoints
GET  /news/fetch?category=Tech&limit=20&offset=0
GET  /news/featured
GET  /news/trending?limit=3
GET  /news/search?q=query

# Chat Endpoints
POST /chat/message
     Body: {"message": "...", "conversation_id": "..."}
DELETE /chat/conversation/:id
GET  /chat/health

# Agent Endpoints
GET  /agent/ingest?url=<URL>
GET  /scraper/cron
```

### Backend API (Port 5000)

```bash
# Article Endpoints
GET  /api/articles?category=Tech&limit=20&offset=0
GET  /api/articles/:id
GET  /api/featured
GET  /api/trending?limit=3
GET  /api/search?q=query

# Newsletter
POST /api/newsletter
     Body: {"email": "user@example.com"}

# Chat Endpoints
POST /api/chat/message
     Body: {"message": "...", "conversation_id": "..."}
DELETE /api/chat/conversation/:id
GET  /api/chat/health
```

## File Locations

```
Project Root
├── GenAI-with-Agentic-AI/     # AI Service
├── Backend/                    # API Gateway
├── Frontend/                   # UI
├── logs/                       # Service logs
├── start-all.sh               # Startup script
├── ingest-news.py             # Data ingestion
├── README.md                  # Main documentation
├── SETUP_GUIDE.md             # Detailed setup
└── ARCHITECTURE_CHANGES.md    # Architecture info
```

## Environment Variables

### Backend/.env
```env
PORT=5000
GENAI_SERVICE_URL=http://localhost:8000
```

## Useful Scripts

### Check Services Status
```bash
# Check if services are running
lsof -i :8000  # GenAI
lsof -i :5000  # Backend
lsof -i :5173  # Frontend
```

### Restart Individual Service

```bash
# Restart GenAI
cd GenAI-with-Agentic-AI
python -m uvicorn app.main:app --reload --port 8000

# Restart Backend
cd Backend
npm run dev

# Restart Frontend
cd Frontend
npm run dev
```

## Testing Chatbot

### Simple Test
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top stories?"}'
```

### With Conversation
```bash
# First message
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about technology news"}' \
  | jq '.conversation_id'

# Follow-up (use conversation_id from above)
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me more", "conversation_id": "conv_xyz"}'
```

## Categories

Available categories:
- Technology
- Business
- Health
- Science
- Sports
- Entertainment
- General

## Tips

1. **Always ingest articles first** before testing the UI
2. **Check logs** if something isn't working
3. **Use start-all.sh** for easy startup
4. **Monitor VectorDB** size as you add more articles
5. **Clear browser cache** if UI seems stale
6. **Use semantic search** - it's smarter than keyword search!

## Need More Help?

- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- See [ARCHITECTURE_CHANGES.md](ARCHITECTURE_CHANGES.md) for system design
- Check service logs in `./logs/` directory
- Verify all services are running with `lsof -i :<PORT>`

---

**Happy Building! 🚀**
