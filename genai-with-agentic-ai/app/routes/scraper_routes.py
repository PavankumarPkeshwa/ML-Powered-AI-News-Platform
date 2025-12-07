from fastapi import APIRouter, Query, BackgroundTasks
import sys
sys.path.insert(0, '/workspaces/ML-Powered-AI-News-Platform/genai-with-agentic-ai')
from scraper.fetcher import scrape_single
from scraper.cleaner import run_cron_job
from agents.supervisor_agent import auto_collect_news, populate_with_samples
import asyncio

router = APIRouter(prefix="/scraper", tags=["Scraper"])

@router.get("/scrape")
def scrape_url(url: str = Query(...)):
    return scrape_single(url)

@router.get("/cron")
def cron_run():
    return run_cron_job()

@router.post("/collect-news")
async def collect_news_now(quick_mode: bool = True, clear_old: bool = False):
    """
    Manually trigger news collection from all sources.
    
    Args:
        quick_mode: If True, collect fewer articles (faster)
        clear_old: If True, clear old articles before collecting new ones
    """
    try:
        stats = await auto_collect_news(quick_mode=quick_mode, clear_old=clear_old)
        total = sum(stats.values())
        return {
            "status": "success",
            "message": f"Collected {total} articles",
            "details": stats,
            "cleared_old": clear_old
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/refresh-news")
async def refresh_all_news():
    """
    Refresh all news: Clear old articles and fetch fresh ones.
    This is like a complete database refresh.
    """
    try:
        stats = await auto_collect_news(quick_mode=False, clear_old=True)
        total = sum(stats.values())
        return {
            "status": "success",
            "message": f"Database refreshed with {total} fresh articles",
            "details": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/populate-samples")
def populate_sample_articles():
    """
    Populate the database with sample articles.
    Useful for testing or when scraping is not available.
    """
    try:
        count = populate_with_samples()
        return {
            "status": "success",
            "message": f"Added {count} sample articles",
            "count": count
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
