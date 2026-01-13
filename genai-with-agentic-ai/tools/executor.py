"""
Simple tool executor with timeouts and safe-fetch wrapper placeholders.
"""
import requests
import logging

logger = logging.getLogger(__name__)


def safe_fetch(url: str, timeout: int = 10):
    """Fetch URL with basic safety constraints (robots.txt respected should be added).
    This is a minimal wrapper — expand for production use.
    """
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "AgenticNewsBot/1.0"})
        r.raise_for_status()
        return r.text
    except Exception as e:
        logger.warning(f"safe_fetch failed for {url}: {e}")
        return None
