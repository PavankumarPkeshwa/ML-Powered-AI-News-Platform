from fastapi import APIRouter, Query, BackgroundTasks
from app.scraper.scraper import scrape_single
from app.scraper.cron import run_cron_job
from app.auto_collector import auto_collect_news, populate_with_samples
import asyncio

router = APIRouter(prefix="/scraper", tags=["Scraper"])

@router.get("/scrape")
def scrape_url(url: str = Query(...)):
    return scrape_single(url)

@router.get("/cron")
def cron_run():
    return run_cron_job()

@router.post("/collect-news")
async def collect_news_now(quick_mode: bool = True):
    """
    Manually trigger news collection from all sources.
    
    Args:
        quick_mode: If True, collect fewer articles (faster)
    """
    try:
        stats = await auto_collect_news(quick_mode=quick_mode)
        total = sum(stats.values())
        return {
            "status": "success",
            "message": f"Collected {total} articles",
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
