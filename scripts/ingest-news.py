#!/usr/bin/env python3
"""
Sample script to ingest news articles into the system.
Run this after starting all services to populate the VectorDB with news.
"""

import requests
import sys
from typing import List

GENAI_URL = "http://localhost:8000"

# Sample news URLs to ingest (replace with real news URLs)
SAMPLE_NEWS_URLS: List[str] = [
    "https://www.bbc.com/news/technology",
    "https://techcrunch.com/2024/01/15/example-tech-article/",
    "https://www.theverge.com/tech",
    "https://arstechnica.com/gadgets/",
    "https://www.reuters.com/technology/",
]

def ingest_article(url: str) -> dict:
    """Ingest a single article."""
    try:
        print(f"📰 Ingesting: {url}")
        response = requests.get(f"{GENAI_URL}/agent/ingest", params={"url": url}, timeout=30)
        result = response.json()
        
        if result.get("status") == "ingested":
            print(f"✅ Success: {result.get('metadata', {}).get('title', 'Unknown')}")
            print(f"   Length: {result.get('metadata', {}).get('length', 0)} words")
        elif result.get("status") == "rejected":
            print(f"⚠️  Rejected: {result.get('reason', 'Unknown reason')}")
        else:
            print(f"❌ Error: {result.get('reason', 'Unknown error')}")
        
        return result
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"status": "error", "reason": str(e)}

def check_service_health() -> bool:
    """Check if GenAI service is running."""
    try:
        response = requests.get(f"{GENAI_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ GenAI Service is running!")
            return True
    except Exception:
        pass
    
    print("❌ GenAI Service is not running. Please start it first:")
    print("   cd GenAI-with-Agentic-AI")
    print("   python -m uvicorn app.main:app --reload --port 8000")
    return False

def main():
    print("╔════════════════════════════════════════════════════╗")
    print("║     News Ingestion Script                          ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    
    # Check service health
    if not check_service_health():
        sys.exit(1)
    
    print()
    print("Starting news ingestion...")
    print()
    
    # Ingest articles
    successful = 0
    failed = 0
    
    for url in SAMPLE_NEWS_URLS:
        result = ingest_article(url)
        if result.get("status") == "ingested":
            successful += 1
        else:
            failed += 1
        print()
    
    # Summary
    print("╔════════════════════════════════════════════════════╗")
    print("║               Ingestion Summary                    ║")
    print("╚════════════════════════════════════════════════════╝")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed:     {failed}")
    print()
    
    if successful > 0:
        print("🎉 Articles have been ingested!")
        print("You can now view them in the frontend: http://localhost:5173")
    else:
        print("⚠️  No articles were successfully ingested.")
        print("Please check the URLs or try different news sources.")

if __name__ == "__main__":
    main()
