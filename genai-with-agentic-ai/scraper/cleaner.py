import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.fetcher import scrape_single

CRON_URLS = [
    "https://www.bbc.com/news",
    "https://www.aljazeera.com/news/",
]

def run_cron_job():
    results = []
    for url in CRON_URLS:
        try:
            results.append(scrape_single(url))
        except Exception as e:
            results.append({"url": url, "error": str(e)})
    return {"cron_results": results}
