"""
workers/scraper_worker.py
Worker tasks for handling collection and ingestion tasks.
This file provides `handle_task` which is callable by RQ or direct invocation.
"""
import logging
import asyncio
from typing import Dict, Any

logger = logging.getLogger(__name__)

from agents import supervisor_agent
from memory import episode_store


def handle_task(task_type: str, payload: Dict[str, Any]):
    """Dispatch a task by type. Synchronous entrypoint used by RQ or direct calls."""
    logger.info(f"Worker received task: {task_type}")
    if task_type == "collect_source":
        return collect_source_task(payload)
    elif task_type == "ingest_url":
        return ingest_url_task(payload)
    else:
        raise ValueError(f"Unknown task type: {task_type}")


def collect_source_task(payload: Dict[str, Any]):
    """Collect from a single source using existing supervisor logic."""
    source = payload.get("source")
    category = payload.get("category", "General")
    max_articles = payload.get("max_articles", 3)

    # supervisor_agent.collect_from_source is async — run it
    try:
        res = asyncio.run(supervisor_agent.collect_from_source(source, category, max_articles))
        # Log episode
        episode_store.log_episode({
            "task": "collect_source",
            "source": source,
            "category": category,
            "result": res,
        })
        return res
    except Exception as e:
        logger.error(f"Error in collect_source_task: {e}")
        episode_store.log_episode({
            "task": "collect_source",
            "source": source,
            "category": category,
            "error": str(e),
        })
        return {"error": str(e)}


def ingest_url_task(payload: Dict[str, Any]):
    url = payload.get("url")
    category = payload.get("category", "General")
    try:
        res = supervisor_agent.ingest_url(url, category)
        episode_store.log_episode({"task": "ingest_url", "url": url, "result": res})
        return res
    except Exception as e:
        logger.error(f"Error in ingest_url_task: {e}")
        episode_store.log_episode({"task": "ingest_url", "url": url, "error": str(e)})
        return {"error": str(e)}
