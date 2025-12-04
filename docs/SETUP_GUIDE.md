# ML-Powered AI News Platform - Setup Guide

## Architecture Overview

This application consists of three main components:

1. **GenAI with Agentic AI** (Python/FastAPI) - Intelligent news scraping, processing, and AI chatbot
2. **Backend** (Node.js/Express) - API gateway that connects frontend to GenAI services
3. **Frontend** (React/TypeScript) - User interface with news display and AI chatbot

### Data Flow

```
News Sources → GenAI Agents → VectorDB → Backend API → Frontend UI
                    ↓
              AI Chatbot (RAG)
```

## Setup Instructions

### 1. GenAI Service (Port 8000)

```bash
cd GenAI-with-Agentic-AI

# Install dependencies
pip install -r requirements.txt

# Start the service
python -m uvicorn app.main:app --reload --port 8000
```

**Available Endpoints:**
- `GET /` - Health check
- `POST /agent/ingest?url=<news_url>` - Scrape and ingest news article
- `GET /scraper/cron` - Run batch news scraping
- `GET /news/fetch?category=&limit=20&offset=0` - Get news articles
- `GET /news/featured` - Get featured article
- `GET /news/trending?limit=3` - Get trending articles
- `GET /news/search?q=<query>` - Search articles
- `POST /chat/message` - Send message to AI chatbot
- `GET /chat/health` - Check chatbot health

### 2. Backend Service (Port 5000)

```bash
cd Backend

# Create .env file
cp .env.example .env

# Edit .env if needed
# GENAI_SERVICE_URL=http://localhost:8000

# Install dependencies
npm install

# Start the server
npm run dev
```

**Available Endpoints:**
- `GET /api/articles?category=&limit=20&offset=0` - Get articles
- `GET /api/articles/:id` - Get article by ID
- `GET /api/featured` - Get featured article
- `GET /api/trending?limit=3` - Get trending articles
- `GET /api/search?q=<query>` - Search articles
- `POST /api/newsletter` - Subscribe to newsletter
- `POST /api/chat/message` - Send chat message
- `DELETE /api/chat/conversation/:id` - Clear conversation
- `GET /api/chat/health` - Chatbot health

### 3. Frontend Service (Port 5173)

```bash
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Access the application at: http://localhost:5173

## First-Time Setup

### Step 1: Start Services

Open 3 terminal windows:

**Terminal 1 - GenAI Service:**
```bash
cd GenAI-with-Agentic-AI
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Backend:**
```bash
cd Backend
npm run dev
```

**Terminal 3 - Frontend:**
```bash
cd Frontend
npm run dev
```

### Step 2: Ingest News Articles

The agents need to fetch news articles first. You can do this by:

**Option A: Using the GenAI API directly**
```bash
# Ingest a single article
curl "http://localhost:8000/agent/ingest?url=https://example.com/news-article"

# Run batch scraping (if configured)
curl "http://localhost:8000/scraper/cron"
```

**Option B: Using Python script**
```python
import requests

# Ingest news from various sources
news_urls = [
    "https://www.bbc.com/news/technology",
    "https://techcrunch.com/latest",
    "https://www.theverge.com/tech",
]

for url in news_urls:
    response = requests.get(f"http://localhost:8000/agent/ingest?url={url}")
    print(response.json())
```

### Step 3: Use the Application

1. Open http://localhost:5173 in your browser
2. Browse news articles fetched by the agents
3. Click the chat icon (bottom-right) to interact with the AI chatbot
4. Ask questions about the news articles

## Features

### 🤖 Agentic AI System

The GenAI service uses multiple specialized agents:

- **News Agent**: Fetches and extracts content from URLs
- **Validator Agent**: Validates article quality and relevance
- **Manager Agent**: Orchestrates the workflow
- **RAG System**: Provides context-aware responses using VectorDB

### 💬 AI Chatbot

- Semantic search across all news articles
- Context-aware conversations
- Source attribution
- Conversation history

### 📰 News Display

- Category filtering
- Featured articles
- Trending news
- Search functionality
- Responsive design

## Key Differences from Previous Version

### ❌ Removed:
- MongoDB database
- Mongoose models
- Manual data seeding
- Static article storage

### ✅ Added:
- GenAI Agentic AI integration
- Vector database for semantic search
- AI-powered chatbot with RAG
- Real-time news scraping
- Intelligent article processing

## Troubleshooting

### Backend can't connect to GenAI service
- Ensure GenAI service is running on port 8000
- Check the `GENAI_SERVICE_URL` in Backend/.env

### No articles showing in UI
- Ingest some news articles using the agent endpoints
- Check GenAI service logs for errors
- Verify VectorDB is initialized

### Chatbot not responding
- Check if VectorDB has articles
- Verify LLM service is running
- Check GenAI service logs

### Port conflicts
- Change ports in respective config files:
  - GenAI: `uvicorn app.main:app --port <PORT>`
  - Backend: `.env` file `PORT=<PORT>`
  - Frontend: `vite.config.ts`

## Environment Variables

### Backend (.env)
```env
PORT=5000
GENAI_SERVICE_URL=http://localhost:8000
```

### GenAI Service
Configure in your local environment or `.env`:
- LLM settings
- VectorDB path
- Scraping configuration

## API Flow Example

### Fetching Articles
```
Frontend → GET /api/articles
    ↓
Backend → GET http://localhost:8000/news/fetch
    ↓
GenAI Service → Query VectorDB → Return formatted articles
    ↓
Backend → Return to Frontend
    ↓
Frontend → Display articles
```

### Chatbot Interaction
```
Frontend → POST /api/chat/message {message: "What's the latest tech news?"}
    ↓
Backend → POST http://localhost:8000/chat/message
    ↓
GenAI Service → RAG Chain → VectorDB Query → LLM Response
    ↓
Backend → Return response with sources
    ↓
Frontend → Display in chat UI
```

## Development Tips

1. **Populate VectorDB**: Always ingest articles before testing
2. **Check Logs**: Monitor all three services for errors
3. **CORS**: GenAI service includes CORS middleware for frontend
4. **Hot Reload**: All services support hot reload during development

## Production Deployment

1. Set up proper CORS origins
2. Use environment-specific URLs
3. Consider Redis for conversation history
4. Implement rate limiting
5. Add authentication for admin endpoints
6. Use persistent VectorDB storage

## Need Help?

- Check service logs for detailed error messages
- Ensure all dependencies are installed
- Verify ports are not in use by other applications
- Test each service independently before integration
