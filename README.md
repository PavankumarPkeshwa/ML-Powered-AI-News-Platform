# ML-Powered AI News Platform

An intelligent news platform powered by AI agents, RAG (Retrieval Augmented Generation), and modern web technologies.

## 🚀 Quick Start

```bash
# Start all services
./scripts/start-all.sh
```

Then open http://localhost:5173 in your browser!

## ✨ Features

- **AI-Powered News Collection**: Automatic news gathering with intelligent agents
- **RAG Chatbot**: Ask questions about articles using advanced AI
- **Smart Categorization**: Technology, Business, Science, Health, Sports, Entertainment
- **Vector Search**: Semantic search powered by ChromaDB
- **Real-time Updates**: Fresh content with automated collection
- **Beautiful UI**: Modern, responsive design with Tailwind CSS

## 📁 Project Structure

```
ML-Powered-AI-News-Platform/
├── Backend/                 # Node.js Express API Gateway
├── Frontend/                # React + TypeScript + Vite
├── GenAI-with-Agentic-AI/  # Python FastAPI with RAG & AI Agents
├── shared/                  # Shared TypeScript schemas
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
└── logs/                    # Application logs
```

## 🛠️ Technology Stack

### Backend Services
- **GenAI Service** (Port 8000): FastAPI, LangChain, ChromaDB, Sentence Transformers
- **Backend API** (Port 5000): Node.js, Express, Axios
- **Frontend** (Port 5173): React, TypeScript, Vite, TanStack Query, Tailwind CSS

### AI Components
- **RAG System**: Retrieval Augmented Generation for intelligent responses
- **Vector Database**: ChromaDB for semantic search
- **LLM**: Flan-T5 (local, no API keys needed)
- **Embeddings**: all-MiniLM-L6-v2 (HuggingFace)

## 📚 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation and configuration
- [Quick Reference](docs/QUICK_REFERENCE.md) - Common commands and troubleshooting
- [System Flow](docs/SYSTEM_FLOW.md) - Architecture and data flow
- [News Sources Info](docs/NEWS_SOURCE_INFO.md) - Where articles come from
- [Project Summary](docs/PROJECT_SUMMARY.md) - Complete feature overview

## 🎯 Key Features Explained

### 1. Automatic News Collection
The system automatically populates with 18 high-quality sample articles on startup:
- 3 articles per category
- Realistic, professionally written content
- Proper metadata and categorization

### 2. AI Chatbot
Ask questions about articles using natural language:
- Context-aware responses
- Source attribution
- Conversation memory
- Powered by local LLM (no API keys required)

### 3. Category-Based Navigation
Browse news by category with proper color coding:
- 🟣 Technology - AI, quantum computing, innovations
- 🔵 Business - Markets, investments, economy
- 🔷 Science - Discoveries, research, space
- 🟢 Health - Medical breakthroughs, wellness
- 🟠 Sports - Championships, records, achievements
- 🌸 Entertainment - Movies, music, streaming

## 🚦 Service Status

Check if all services are running:

```bash
# Check GenAI service
curl http://localhost:8000/

# Check Backend
curl http://localhost:5000/api/articles

# Check Frontend
curl http://localhost:5173/
```

## 📝 Development

### Prerequisites
- Node.js 18+
- Python 3.10+
- npm/yarn

### Installation

```bash
# Install Backend dependencies
cd Backend && npm install

# Install Frontend dependencies
cd Frontend && npm install

# Install GenAI dependencies
cd GenAI-with-Agentic-AI && pip install -r requirements.txt
```

### Running Services Individually

```bash
# Start GenAI service
cd GenAI-with-Agentic-AI
python -m uvicorn app.main:app --port 8000

# Start Backend
cd Backend
node server.js

# Start Frontend
cd Frontend
npm run dev
```

## 🔧 Configuration

- Backend env: `Backend/.env`
- GenAI service: `GenAI-with-Agentic-AI/app/auto_collector.py`
- Categories: `shared/schema.ts`

## 🌟 What Makes This Special

1. **No External APIs Required**: Uses local LLM and free embeddings
2. **Intelligent Search**: Vector-based semantic search finds relevant articles
3. **RAG-Powered Chat**: Chatbot answers based on actual article content
4. **Fully Integrated**: Three services work seamlessly together
5. **Production Ready**: Proper error handling, logging, and documentation

## 📊 Article Statistics

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
