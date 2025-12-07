import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.supervisor_agent import ingest_url

def scrape_single(url: str) -> dict:
    return ingest_url(url)
