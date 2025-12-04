# 🤖 ML-Powered AI News Platform

An intelligent news platform powered by **Agentic AI**, **RAG (Retrieval-Augmented Generation)**, and **Vector Databases**. The system uses AI agents to scrape, validate, and deliver news articles, with an integrated AI chatbot for interactive news exploration.

## 🌟 Features

### 🤖 Agentic AI System
- **News Agent**: Automatically scrapes and extracts content from news sources
- **Validator Agent**: Validates article quality, relevance, and authenticity
- **Manager Agent**: Orchestrates the entire workflow
- **RAG System**: Provides intelligent, context-aware responses

### 💬 AI Chatbot
- Semantic search across all news articles
- Context-aware conversations using RAG
- Source attribution for transparency
- Persistent conversation history

### 📰 News Platform
- Real-time news display
- Category filtering (Technology, Business, Health, Science, Sports, Entertainment)
- Featured and trending articles
- Semantic search functionality
- Responsive modern UI

### 🔗 Architecture

```
┌─────────────────┐
│   News Sources  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GenAI Agents   │◄───┐
│  (Scraper +     │    │
│   Validator +   │    │
│   Manager)      │    │
└────────┬────────┘    │
         │             │
         ▼             │
┌─────────────────┐    │
│   Vector DB     │    │
│  (Embeddings)   │    │
└────────┬────────┘    │
         │             │
         ├─────────────┘
         │
         ▼
┌─────────────────┐
│  Backend API    │
│  (Express.js)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frontend UI    │
│  (React + TS)   │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### One-Command Setup

```bash
./start-all.sh
```

This will:
1. Install all dependencies
2. Start GenAI service (port 8000)
3. Start Backend API (port 5000)
4. Start Frontend UI (port 5173)

### Ingest News Articles

Before using the platform, populate it with news:

```bash
python3 ingest-news.py
```

Or manually ingest specific URLs:

```bash
curl "http://localhost:8000/agent/ingest?url=<NEWS_URL>"
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **GenAI Service**: http://localhost:8000

## 📖 Detailed Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for comprehensive setup instructions.

## 🏗️ Project Structure

```
.
├── GenAI-with-Agentic-AI/    # AI service with agents
│   ├── app/
│   │   ├── agent/             # Agent implementations
│   │   │   ├── manager_agent.py
│   │   │   ├── news_agent.py
│   │   │   └── validator_agent.py
│   │   ├── rag/               # RAG system
│   │   │   ├── embedder.py
│   │   │   ├── vectordb.py
│   │   │   └── rag_chain.py
│   │   ├── routes/            # API routes
│   │   │   ├── news_routes.py    # News endpoints
│   │   │   ├── chat_routes.py    # Chatbot endpoints
│   │   │   ├── agent_routes.py
│   │   │   └── scraper_routes.py
│   │   └── main.py            # FastAPI app
│   └── requirements.txt
│
├── Backend/                   # Node.js API gateway
│   ├── controllers/
│   │   ├── articleController.js
│   │   └── chatController.js
│   ├── routes/
│   │   ├── articleRoutes.js
│   │   └── chatRoutes.js
│   ├── app.js
│   └── server.js
│
├── Frontend/                  # React UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── chatbot.tsx    # AI Chatbot component
│   │   │   ├── article-card.tsx
│   │   │   └── ...
│   │   ├── pages/
│   │   ├── lib/
│   │   │   └── api.ts         # API client
│   │   └── App.tsx
│   └── package.json
│
├── start-all.sh              # Quick start script
├── ingest-news.py            # News ingestion script
└── SETUP_GUIDE.md            # Detailed setup guide
```

## 🔧 Manual Setup

### 1. GenAI Service

```bash
cd GenAI-with-Agentic-AI
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Backend

```bash
cd Backend
npm install
cp .env.example .env
npm run dev
```

### 3. Frontend

```bash
cd Frontend
npm install
npm run dev
```

## 🎯 Key Endpoints

### GenAI Service (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/news/fetch` | Get news articles |
| GET | `/news/featured` | Get featured article |
| GET | `/news/trending` | Get trending articles |
| GET | `/news/search?q=query` | Search articles |
| POST | `/chat/message` | Send message to AI chatbot |
| POST | `/agent/ingest?url=URL` | Ingest news article |
| GET | `/scraper/cron` | Run batch scraping |

### Backend API (Port 5000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles` | Get all articles |
| GET | `/api/articles/:id` | Get article by ID |
| GET | `/api/featured` | Get featured article |
| GET | `/api/trending` | Get trending articles |
| GET | `/api/search?q=query` | Search articles |
| POST | `/api/chat/message` | Chat with AI |
| POST | `/api/newsletter` | Subscribe to newsletter |

## 💡 Usage Examples

### Chatbot Usage

1. Click the chat icon in the bottom-right corner
2. Ask questions like:
   - "What's the latest in technology?"
   - "Summarize the trending news"
   - "Tell me about AI developments"
3. The chatbot uses RAG to provide accurate, sourced responses

### Ingesting Custom News

```python
import requests

url = "https://example.com/news-article"
response = requests.get(f"http://localhost:8000/agent/ingest?url={url}")
print(response.json())
```

### Searching News

```bash
curl "http://localhost:5000/api/search?q=artificial+intelligence"
```

## 🔒 Key Differences from Traditional Systems

### ❌ What We DON'T Use:
- ❌ MongoDB or traditional databases
- ❌ Manual data entry or seeding
- ❌ Static article storage
- ❌ Simple keyword matching

### ✅ What We USE:
- ✅ **Vector Database** for semantic search
- ✅ **AI Agents** for intelligent scraping
- ✅ **RAG** for context-aware responses
- ✅ **LLM** for content validation and chat
- ✅ **Embeddings** for similarity search
- ✅ **Real-time processing** by agents

## 🛠️ Technology Stack

### GenAI Service
- **Framework**: FastAPI
- **AI**: LangChain, Local LLM
- **Vector DB**: Chroma/FAISS
- **Embeddings**: Sentence Transformers
- **Agents**: Custom agent architecture

### Backend
- **Framework**: Express.js
- **HTTP Client**: Axios
- **Language**: JavaScript (Node.js)

### Frontend
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State**: TanStack Query
- **Routing**: Wouter

## 🐛 Troubleshooting

### No articles showing?
1. Make sure GenAI service is running
2. Run `python3 ingest-news.py` to populate articles
3. Check logs in `./logs/` directory

### Chatbot not responding?
1. Verify VectorDB has articles
2. Check GenAI service logs
3. Ensure LLM is properly configured

### Port conflicts?
```bash
# Kill processes on specific ports
lsof -ti:8000 | xargs kill -9  # GenAI
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
```

## 📝 Environment Variables

### Backend (.env)
```env
PORT=5000
GENAI_SERVICE_URL=http://localhost:8000
```

### GenAI Service
Configure in your environment:
- LLM settings
- VectorDB path
- Embedding model
- Scraping configuration

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License

## 🙏 Acknowledgments

- Built with LangChain for RAG implementation
- UI components from shadcn/ui
- Powered by local LLM and embeddings

---

**Made with ❤️ using Agentic AI and RAG**

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
