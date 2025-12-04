from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

# Importing our route modules
# Each route file will contain endpoints for RAG, Agents, Scraper
from app.routes import rag_routes, agent_routes, scraper_routes, news_routes, chat_routes
from app.auto_collector import initialize_news_collection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="GenAI News Intelligence API",
    description="RAG + Agentic AI + Scraper + VectorDB + News + Chatbot",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(rag_routes.router)
app.include_router(agent_routes.router)
app.include_router(scraper_routes.router)
app.include_router(news_routes.router)
app.include_router(chat_routes.router)


# Startup event - automatically collect news
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    Automatically populates the database with news articles.
    """
    logger.info("🚀 Starting GenAI News Service...")
    logger.info("📰 Initializing automatic news collection...")
    
    # Run news collection in background
    asyncio.create_task(initialize_news_collection(use_samples=True))
    
    logger.info("✅ Service ready! News collection running in background.")


# Root sanity check
@app.get("/")
def home():
    return {
        "status": "GenAI Service Running 🚀", 
        "endpoints": ["/news", "/chat", "/agent", "/scraper", "/rag"],
        "features": ["Auto News Collection", "AI Chatbot", "Agentic Processing"]
    }
