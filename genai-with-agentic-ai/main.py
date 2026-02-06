# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import asyncio
# import logging
# from dotenv import load_dotenv
# import sys
# import os

# # Add current directory to path for imports
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# # Load environment variables from .env file
# load_dotenv()

# # Verify HuggingFace token is loaded
# hf_token = os.getenv("HUGGINGFACE_TOKEN")
# if hf_token:
#     print(f"✅ HuggingFace token loaded: {hf_token[:10]}...")
# else:
#     print("⚠️ No HuggingFace token found - will use free models only")

# # Importing our route modules
# # Each route file will contain endpoints for RAG, Agents, Scraper
# from app.routes import rag_routes, agent_routes, scraper_routes
# from api import news_api, chat_api
# from agents.supervisor_agent import initialize_news_collection

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Create FastAPI instance
# app = FastAPI(
#     title="GenAI News Intelligence API",
#     description="RAG + Agentic AI + Scraper + VectorDB + News + Chatbot",
#     version="1.0.0"
# )

# # Add CORS middleware for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include all API routes
# app.include_router(rag_routes.router)
# app.include_router(agent_routes.router)
# app.include_router(scraper_routes.router)
# app.include_router(news_api.router)
# app.include_router(chat_api.router)


# # Startup event - automatically collect news
# @app.on_event("startup")
# async def startup_event():
#     """
#     Run on application startup.
#     Automatically collects REAL news from internet using AI agents.
#     Sets up periodic news collection every 6 hours.
#     """
#     logger.info("🚀 Starting GenAI News Service...")
#     logger.info("📰 AI-powered news collection ready")
#     logger.info("🤖 AI Agents: News Scraper → Validator → VectorDB Storage")
    
#     # Start periodic collection (every 6 hours) - first run will happen after 6 hours
#     from agents.supervisor_agent import periodic_news_collection
#     # Trigger an initial collection in background so UI has content on first run.
#     # `initialize_news_collection` will try real collection and optionally fall back to samples.
#     try:
#         from agents.supervisor_agent import initialize_news_collection
#         # Do not load sample articles on startup; only populate UI when real scraping succeeds
#         asyncio.create_task(initialize_news_collection(use_samples=False))
#     except Exception:
#         logger.warning("⚠️ Could not schedule initial collection task")

#     asyncio.create_task(periodic_news_collection(interval_hours=6))
    
#     logger.info("✅ Service ready!")
#     logger.info("⏰ Automatic news updates every 6 hours")
#     logger.info("💡 Trigger manual collection: POST /scraper/refresh-news")


# # Root sanity check
# @app.get("/")
# def home():
#     return {
#         "status": "GenAI Service Running 🚀", 
#         "endpoints": ["/news", "/chat", "/agent", "/scraper", "/rag"],
#         "features": ["Auto News Collection", "AI Chatbot", "Agentic Processing"]
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Path fix for HF
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load env
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="GenAI News Intelligence API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
from api import news_api, chat_api
from app.routes import rag_routes, agent_routes, scraper_routes

app.include_router(rag_routes.router)
app.include_router(agent_routes.router)
app.include_router(scraper_routes.router)
app.include_router(news_api.router)
app.include_router(chat_api.router)

# IMPORTANT IMPORT
from cache.build_news_cache import build_news_cache
from agents.supervisor_agent import (
    initialize_news_collection,
    periodic_news_collection
)

# -----------------------------
# CORE PIPELINE (NO CONFUSION)
# -----------------------------
async def collect_news_and_build_cache():
    """
    1. Scrape news
    2. Store in VectorDB
    3. Build JSON cache for UI
    """
    try:
        logger.info("🧠 Collecting news into VectorDB...")
        await initialize_news_collection(use_samples=False)

        logger.info("📦 Building JSON cache from VectorDB...")
        build_news_cache()

        logger.info("✅ JSON cache ready")
    except Exception as e:
        logger.error(f"❌ News pipeline failed: {e}")


# -----------------------------
# STARTUP EVENT (HF SAFE)
# -----------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 GenAI News Service starting...")

    # First run immediately
    asyncio.create_task(collect_news_and_build_cache())

    # Repeat every 6 hours
    asyncio.create_task(periodic_news_collection(interval_hours=2))

    logger.info("⏰ News refresh scheduled every 2 hours")


# -----------------------------
# ROOT CHECK
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "GenAI Service Running",
        "features": ["Scraper", "VectorDB", "JSON Cache", "Fast UI"]
    }
