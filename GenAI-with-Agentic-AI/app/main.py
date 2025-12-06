from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify HuggingFace token is loaded
import os
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if hf_token:
    print(f"✅ HuggingFace token loaded: {hf_token[:10]}...")
else:
    print("⚠️ No HuggingFace token found - will use free models only")

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
    Automatically collects REAL news from internet using AI agents.
    """
    logger.info("🚀 Starting GenAI News Service...")
    logger.info("📰 Initializing AI-powered news collection...")
    logger.info("🤖 AI Agents: News Scraper → Validator → VectorDB Storage")
    
    # Run REAL news collection with agents (samples only as last resort)
    asyncio.create_task(initialize_news_collection(use_samples=False))
    
    logger.info("✅ Service ready! AI agents collecting real news in background.")


# Root sanity check
@app.get("/")
def home():
    return {
        "status": "GenAI Service Running 🚀", 
        "endpoints": ["/news", "/chat", "/agent", "/scraper", "/rag"],
        "features": ["Auto News Collection", "AI Chatbot", "Agentic Processing"]
    }
