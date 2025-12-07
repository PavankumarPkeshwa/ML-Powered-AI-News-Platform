# 🤖 ML-Powered AI News Platform

A fully intelligent news aggregation platform powered by **AI Agents**, **RAG (Retrieval Augmented Generation)**, **RSS Feed Collection**, and **Llama 3.2 LLM**. The system automatically collects real news articles from the internet using AI agents and provides an intelligent chatbot for news queries.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/PavankumarPkeshwa/ML-Powered-AI-News-Platform.git
cd ML-Powered-AI-News-Platform

# Install dependencies
cd Backend && npm install && cd ..
cd Frontend && npm install && cd ..
cd genai-with-agentic-ai && pip install -r requirements.txt && cd ..

# (Optional) Enable Llama 3.2 for better chatbot responses
# Create .env file in genai-with-agentic-ai/ with your HuggingFace token
# See Configuration section below for details

# Start all services (works with or without .env!)
./scripts/start-all.sh

# Check service status
./scripts/check-status.sh
```

Then open **http://localhost:5173** in your browser!

> 💡 **Note**: No `.env` file required! App works out-of-the-box. Add HuggingFace token later for enhanced chatbot responses.

## ✨ Key Features

### 🌐 Real News Collection
- **RSS Feed Integration**: Automatically collects from TechCrunch, The Verge, BBC, CNBC, ESPN, Variety, and more
- **AI Agent Pipeline**: Manager Agent → News Scraper → Validator → VectorDB
- **Article Discovery**: Intelligent parsing of RSS feeds and homepage article links
- **30+ Sources**: Across Technology, Business, Science, Health, Sports, Entertainment

### 🤖 Intelligent Chatbot (Dual-Mode)
- **List Mode**: "Show me latest technology news" → Returns top 10 articles
- **Analytical Mode**: "Will AI kill human jobs?" → Llama 3.2 provides reasoning with article references
- **Category Filtering**: Asks about specific categories (health, tech, etc.)
- **Powered by Llama 3.2-3B-Instruct** via HuggingFace Inference API

### 🔍 Advanced Features
- **RAG System**: Retrieval Augmented Generation for context-aware responses
- **Vector Search**: Semantic search powered by ChromaDB + Sentence Transformers
- **Real-time Updates**: Automated news collection every 6 hours
- **Smart Categorization**: AI-powered category assignment
- **Beautiful UI**: Modern React + Tailwind CSS design

## 📁 Project Structure

```
ML-Powered-AI-News-Platform/
├── Backend/                 # Node.js Express API Gateway
├── Frontend/                # React + TypeScript + Vite
├── genai-with-agentic-ai/  # Python FastAPI with RAG & AI Agents
├── shared/                  # Shared TypeScript schemas
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
└── logs/                    # Application logs
```

## 🛠️ Technology Stack

### Backend Services
- **GenAI Service** (Port 8000): Python FastAPI, LangChain, ChromaDB, Sentence Transformers
- **Backend API** (Port 5000): Node.js, Express (API Gateway)
- **Frontend** (Port 5173): React 18, TypeScript, Vite, TanStack Query, Tailwind CSS

### AI & ML Components
- **LLM**: Llama 3.2-3B-Instruct (HuggingFace Inference API - Serverless)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Database**: ChromaDB for semantic search
- **RAG System**: LangChain for document processing and retrieval
- **News Collection**: BeautifulSoup, feedparser, requests
- **AI Agents**: Manager Agent (orchestrator), News Agent (scraper), Validator Agent

### Data Sources (RSS Feeds)
- **Technology**: TechCrunch, The Verge, ArsTechnica, Wired, BBC Tech
- **Business**: BBC Business, CNBC
- **Science**: Scientific American, Phys.org, Science Daily
- **Health**: BBC Health, Medical News Today
- **Sports**: BBC Sport, ESPN
- **Entertainment**: Variety, Deadline, Hollywood Reporter

## 📚 Architecture & Workflow

### System Architecture
```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│  Frontend   │────────>│   Backend    │────────>│   GenAI      │
│  (Port 5173)│         │  (Port 5000) │         │  (Port 8000) │
│  React + UI │<────────│  API Gateway │<────────│  FastAPI     │
└─────────────┘         └──────────────┘         └──────────────┘
                                                          │
                                                          v
                        ┌──────────────────────────────────────┐
                        │  AI Agent Pipeline                   │
                        │  Manager → Scraper → Validator       │
                        └──────────────────────────────────────┘
                                        │
                                        v
                            ┌───────────────────┐
                            │   ChromaDB        │
                            │   Vector Storage  │
                            └───────────────────┘
```

### News Collection Workflow

1. **Startup** (`app/main.py`)
   - GenAI service initializes
   - Calls `initialize_news_collection(use_samples=False)`
   - Prioritizes real news over sample articles

2. **Auto Collector** (`app/auto_collector.py`)
   - Reads RSS feeds from 30+ news sources
   - Parses feeds using `feedparser` library
   - Extracts article URLs (3-5 per source)
   - Passes to Manager Agent

3. **Manager Agent** (`app/agent/manager_agent.py`)
   - Orchestrates the ingestion pipeline
   - Calls News Agent to fetch and clean content
   - Generates rich metadata (title, category, tags, etc.)
   - Stores in ChromaDB with proper categorization

4. **News Agent** (`app/agent/news_agent.py`)
   - Fetches HTML from article URLs
   - Extracts main text using BeautifulSoup
   - Parses titles from HTML tags
   - Returns cleaned content

5. **Storage** (`app/rag/vectordb.py`)
   - Converts articles to embeddings
   - Stores in ChromaDB with metadata
   - Enables semantic search

### Chatbot Workflow

1. **User Query** → Frontend sends to Backend → Backend forwards to GenAI

2. **Query Analysis** (`app/routes/chat_routes.py`)
   ```python
   detect_query_type(message)
   # Returns: "list" or "analytical"
   
   detect_category(message)  
   # Returns: Technology, Health, Business, etc.
   ```

3. **List Mode** (e.g., "Show latest tech news")
   - Searches VectorDB by category
   - Returns top 10 articles directly
   - Fast response (~100ms)

4. **Analytical Mode** (e.g., "Will AI replace jobs?")
   - Searches VectorDB for relevant articles (top 3)
   - Builds context from article content
   - Calls Llama 3.2 via HuggingFace API
   - Returns AI-generated answer + references

## 📂 Detailed File Structure & Roles

### Backend (Node.js API Gateway)
```
Backend/
├── server.js                  # Express server entry point
├── app.js                     # App configuration & middleware
├── controllers/
│   ├── articleController.js   # Proxies requests to GenAI service
│   └── chatController.js      # Proxies chat requests to GenAI
├── models/
│   └── articleModel.js        # Article schema (unused, GenAI handles DB)
└── routes/
    ├── articleRoutes.js       # /api/articles endpoints
    └── chatRoutes.js          # /api/chat endpoints
```

**Key Endpoints:**
- `GET /api/articles` → Fetches all articles from GenAI
- `GET /api/articles/:id` → Fetches single article
- `POST /api/chat` → Sends chat message to GenAI chatbot

### Frontend (React + TypeScript)
```
Frontend/
├── src/
│   ├── main.tsx              # App entry point
│   ├── App.tsx               # Main app component with routing
│   ├── components/
│   │   ├── header.tsx        # Navigation bar
│   │   ├── hero-section.tsx  # Homepage banner
│   │   ├── article-card.tsx  # Article display card
│   │   ├── category-tabs.tsx # Category filter tabs
│   │   ├── chatbot.tsx       # AI chatbot interface (DUAL-MODE)
│   │   ├── search-overlay.tsx# Search functionality
│   │   ├── theme-toggle.tsx  # Dark/light mode switcher
│   │   └── ui/               # Shadcn/ui components
│   ├── pages/
│   │   ├── home.tsx          # Homepage with featured articles
│   │   ├── category.tsx      # Category-filtered view
│   │   ├── article.tsx       # Single article page
│   │   └── admin.tsx         # Admin panel (future)
│   ├── lib/
│   │   ├── api.ts            # Axios instance for API calls
│   │   └── queryClient.ts    # React Query configuration
│   └── hooks/
│       ├── use-mobile.tsx    # Mobile detection hook
│       └── use-toast.ts      # Toast notification hook
```

### GenAI Service (Python FastAPI + AI) - **MODULAR STRUCTURE**
```
genai-with-agentic-ai/
├── main.py                   # FastAPI app entry point
├── agents/                   # AI Agent modules
│   ├── supervisor_agent.py   # Orchestrates collection + manager logic
│   ├── scraper_agent.py      # RSS parser + article scraper
│   └── storage_agent.py      # Content validation before storage
├── api/                      # API route handlers
│   ├── chat_api.py           # /chat/message (DUAL-MODE CHATBOT)
│   └── news_api.py           # /news/fetch, /news/featured
├── rag/                      # RAG (Retrieval Augmented Generation)
│   ├── vectordb.py           # ChromaDB wrapper
│   ├── embedder.py           # Sentence transformer embeddings
│   ├── rag_chain.py          # LangChain RAG pipeline
│   ├── retriever.py          # Document retrieval utilities
│   ├── splitter.py           # Text chunking for large docs
│   └── llm.py                # LLM wrappers (HuggingFace + Local)
├── scraper/                  # News scraping utilities
│   ├── sources.py            # RSS feed configurations
│   ├── fetcher.py            # Web scraping functions
│   └── cleaner.py            # Content cleaning utilities
├── app/routes/               # Legacy route imports (for compatibility)
│   ├── rag_routes.py         # /rag/query
│   ├── agent_routes.py       # /agent/ingest
│   └── scraper_routes.py     # /scraper/cron
└── vector_store/             # ChromaDB persistent storage
```

**Key API Endpoints:**
- `GET /news/fetch?category=Technology&limit=20` → Fetch articles by category
- `GET /news/featured` → Get featured article
- `POST /chat/message` → Chatbot (detects mode: list vs analytical)
- `POST /agent/ingest` → Manually ingest URL
- `GET /scraper/cron` → Manually trigger news collection

## 🎯 How Each Component Works

### 1. RSS Feed Collection (`auto_collector.py`)
```python
# Runs on startup
NEWS_SOURCES = {
    "Technology": [
        {"url": "https://techcrunch.com/feed/", "type": "rss"},
        {"url": "https://www.theverge.com/rss/index.xml", "type": "rss"}
    ],
    # ... more categories
}

# Collects 2-3 sources per category = 30+ articles
await auto_collect_news(quick_mode=False)
```

### 2. Dual-Mode Chatbot (`chat_routes.py`)
```python
def detect_query_type(message):
    # List mode keywords
    if any(word in msg for word in ['latest', 'recent', 'top', 'show me']):
        return "list"
    # Analytical mode for reasoning questions
    return "analytical"

# List Mode: Returns articles directly
if query_type == "list":
    results = vectordb.similarity_search(query, k=10, filter={"category": cat})
    return [{"title": doc.title, "url": doc.url} for doc in results]

# Analytical Mode: Uses Llama 3.2 LLM
else:
    # Get relevant articles
    docs = vectordb.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Call Llama via HuggingFace API
    llm = HuggingFaceAPILLM(model="meta-llama/Llama-3.2-3B-Instruct")
    answer = llm.invoke(prompt_with_context)
    return {"answer": answer, "sources": docs}
```

### 3. Vector Search (`vectordb.py`)
```python
# Convert text to embeddings using sentence-transformers
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Store in ChromaDB with metadata
vectordb.add_documents([
    Document(
        page_content=article_text,
        metadata={
            "title": title,
            "category": "Technology",
            "source": url,
            "publishDate": datetime.now().isoformat()
        }
    )
])

# Semantic search
results = vectordb.similarity_search(
    query="AI innovations",
    k=10,
    filter={"category": "Technology"}
)
```

## 🔧 Configuration & Environment Variables

### GenAI Service (`.env`) - **OPTIONAL**

> ⚠️ **Important**: The `.env` file is **optional**! The application will work without it.
> - **Without token**: Chatbot uses Flan-T5-base (smaller, faster, but weaker responses)
> - **With token**: Chatbot uses Llama 3.2-3B-Instruct (better reasoning and analytical answers)

**To enable Llama 3.2** (optional but recommended):
1. Create `.env` file in `genai-with-agentic-ai/` directory
2. Add your HuggingFace token:
```bash
HUGGINGFACE_TOKEN=hf_your_token_here  # Get free token from huggingface.co/settings/tokens
HF_TOKEN=hf_your_token_here           # Same token (either variable works)
```

**Get your free token**: Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and create a new token.

### Customizing News Sources
Edit `genai-with-agentic-ai/scraper/sources.py`:
```python
NEWS_SOURCES = {
    "YourCategory": [
        {"url": "https://example.com/feed/", "type": "rss"},
        {"url": "https://example.com/news", "type": "discover"}  # HTML parsing
    ]
}
```

## 🚀 How to Run the Application

### Method 1: Quick Start (Recommended)
```bash
# Start all services at once
./scripts/start-all.sh

# Check if all services are running
./scripts/check-status.sh
```

### Method 2: Manual Start (Individual Services)
```bash
# Terminal 1 - Start GenAI Service (Port 8000)
cd genai-with-agentic-ai
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Start Backend (Port 5000)
cd Backend
node server.js

# Terminal 3 - Start Frontend (Port 5173)
cd Frontend
npm run dev
```

### Method 3: Background Start (Production-like)
```bash
# Start in background with logs
cd genai-with-agentic-ai
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../logs/genai.log 2>&1 &

cd Backend
nohup node server.js > ../logs/backend.log 2>&1 &

cd Frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &

# Monitor logs
tail -f logs/*.log
```

## 🔍 Verifying Installation

### Check Service Status
```bash
# Check all services
./scripts/check-status.sh

# Or check individually:
curl http://localhost:8000/              # GenAI: {"status": "GenAI Service Running"}
curl http://localhost:5000/              # Backend: {"status": "Backend Running"}
curl http://localhost:5173/              # Frontend: HTML response
```

### Test News Collection
```bash
# Check collected articles
curl "http://localhost:8000/news/fetch?limit=5" | python3 -m json.tool

# Trigger manual collection
curl http://localhost:8000/scraper/cron

# Check by category
curl "http://localhost:8000/news/fetch?category=Technology&limit=10"
```

### Test Chatbot
```bash
# List mode query
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me latest technology news"}'

# Analytical mode query
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Will AI replace human jobs?"}'
```

## 📝 Development Guide

### Prerequisites
- **Node.js** 18+ (for Backend & Frontend)
- **Python** 3.10+ (for GenAI service)
- **Git** (for cloning)
- **8GB RAM** minimum (for embedding models)

### Initial Setup
```bash
# 1. Clone repository
git clone https://github.com/PavankumarPkeshwa/ML-Powered-AI-News-Platform.git
cd ML-Powered-AI-News-Platform

# 2. Install Backend dependencies
cd Backend
npm install
cd ..

# 3. Install Frontend dependencies
cd Frontend
npm install
cd ..

# 4. Install GenAI dependencies
cd genai-with-agentic-ai
pip install -r requirements.txt
cd ..

# 5. Configure HuggingFace token (optional, for better LLM)
cd genai-with-agentic-ai
echo "HUGGINGFACE_TOKEN=your_hf_token_here" > .env
cd ..

# 6. Make scripts executable
chmod +x scripts/*.sh

# 7. Start all services
./scripts/start-all.sh
```

### Getting HuggingFace Token (Optional)
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (read access)
3. Add to `genai-with-agentic-ai/.env`:
   ```bash
   HUGGINGFACE_TOKEN=hf_YourTokenHere
   HF_TOKEN=hf_YourTokenHere
   ```

## 🌟 What Makes This Platform Special

### ✅ Real News Collection
- **No Hardcoded Data**: All articles scraped from real news sources
- **30+ RSS Feeds**: TechCrunch, BBC, ESPN, Scientific American, etc.
- **Auto-Updates**: Collects fresh articles every startup
- **AI-Powered**: Intelligent agent pipeline validates and categorizes

### ✅ Advanced Chatbot
- **Dual-Mode Intelligence**: Switches between list and analytical modes automatically
- **Llama 3.2 LLM**: State-of-the-art language model via HuggingFace API
- **Context-Aware**: Uses RAG to answer based on actual article content
- **Category Detection**: "Show me health news" → filters by Health category

### ✅ Vector-Powered Search
- **Semantic Search**: Finds articles by meaning, not just keywords
- **ChromaDB**: Fast, persistent vector storage
- **Sentence Transformers**: High-quality embeddings (384 dimensions)
- **Metadata Filtering**: Search within specific categories

### ✅ Production-Ready Architecture
- **Microservices**: Separate Frontend, Backend, GenAI services
- **Error Handling**: Comprehensive logging and error recovery
- **Scalable**: Can add more news sources easily
- **Documented**: Extensive inline comments and documentation

## 🐛 Troubleshooting

### ✅ "Will I Get Errors on Next Run?"
**No! The application will run successfully without any `.env` file.** Here's what happens:

- ✅ **All services start normally** (Frontend, Backend, GenAI)
- ✅ **News collection works** (RSS feeds, AI agents, VectorDB)
- ✅ **Chatbot list mode works** ("show me latest news" → returns articles)
- ⚠️ **Chatbot analytical mode** uses Flan-T5 (weaker model) instead of Llama 3.2
  - Still works, but answers may be shorter/less sophisticated
  - To upgrade: Create `.env` file with your HuggingFace token (see Configuration section)

**No errors, no crashes** - just different LLM quality depending on token availability.

### Services Not Starting
```bash
# Check if ports are already in use
lsof -i :5173  # Frontend
lsof -i :5000  # Backend  
lsof -i :8000  # GenAI

# Kill processes if needed
kill -9 <PID>

# Or use the stop script
pkill -f "uvicorn app.main"
pkill -f "node server.js"
pkill -f "vite"
```

### No Articles Showing
```bash
# Manually trigger news collection
curl http://localhost:8000/scraper/cron

# Check GenAI logs
tail -f logs/genai.log

# Verify VectorDB has articles
curl "http://localhost:8000/news/fetch?limit=5" | python3 -m json.tool
```

### Chatbot Not Responding
```bash
# Check if GenAI service is running
curl http://localhost:8000/

# Test chat endpoint
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check for errors in logs
tail -50 logs/genai.log | grep -i error
```

### Dependencies Issues
```bash
# Backend
cd Backend && npm install --force

# Frontend
cd Frontend && npm install --force

# GenAI - Reinstall with specific versions
cd genai-with-agentic-ai
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📊 Project Statistics

- **Lines of Code**: ~5,000+
- **Services**: 3 (Frontend, Backend, GenAI)
- **API Endpoints**: 15+
- **News Sources**: 30+ RSS feeds
- **Categories**: 6 (Technology, Business, Science, Health, Sports, Entertainment)
- **Average Collection**: 30+ real articles per startup
- **Technologies Used**: 15+ (React, FastAPI, ChromaDB, LangChain, etc.)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Pavankumar Pkeshwa**
- GitHub: [@PavankumarPkeshwa](https://github.com/PavankumarPkeshwa)
- Repository: [ML-Powered-AI-News-Platform](https://github.com/PavankumarPkeshwa/ML-Powered-AI-News-Platform)

## 🙏 Acknowledgments

- **HuggingFace** for Llama 3.2 and embedding models
- **LangChain** for RAG framework
- **ChromaDB** for vector storage
- **FastAPI** for modern Python API framework
- **React Team** for the awesome frontend library
- **TanStack Query** for efficient data fetching
- **Tailwind CSS** for beautiful styling
- **Shadcn/ui** for component library

## 📚 Additional Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation steps
- [Quick Reference](docs/QUICK_REFERENCE.md) - Commands and shortcuts
- [System Flow](docs/SYSTEM_FLOW.md) - Architecture diagrams
- [Chatbot Modes](genai-with-agentic-ai/CHATBOT_MODES.md) - How dual-mode works
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Feature overview

## 🚀 Future Enhancements

- [ ] User authentication and saved articles
- [ ] Social media sharing
- [ ] Article bookmarking
- [ ] Email notifications for new articles
- [ ] Advanced filters (date range, source)
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Article summarization
- [ ] Trending topics detection
- [ ] Personalized recommendations

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

## 📊 Quick Stats

- Total Articles: 18
- Categories: 6
- Average Read Time: 1-2 minutes per article
- Update Frequency: On-demand (configurable for real-time)

## 🔮 Future Enhancements

- [ ] Real-time news scraping from live sources
- [ ] User authentication and personalization
- [ ] Article bookmarking and favorites
- [ ] Social sharing features
- [ ] Advanced search filters
- [ ] Mobile app

## 🤝 Contributing

This is a portfolio/demo project showcasing AI integration in a news platform.

## 📄 License

MIT License - Feel free to use for learning and portfolio purposes.

## �� Acknowledgments

Built with modern AI technologies:
- LangChain for RAG implementation
- ChromaDB for vector storage
- HuggingFace for embeddings
- React ecosystem for beautiful UI

---

**Status**: ✅ Fully Operational | **Version**: 2.0 | **Last Updated**: December 2025
