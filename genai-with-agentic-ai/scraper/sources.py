"""
News Sources Configuration
Defines all RSS feeds and news sources by category
"""

# Default news sources by category (RSS and direct article URLs work better)
NEWS_SOURCES = {
    "Technology": [
        {"url": "https://techcrunch.com/feed/", "type": "rss"},
        {"url": "https://www.theverge.com/rss/index.xml", "type": "rss"},
        {"url": "https://feeds.arstechnica.com/arstechnica/index", "type": "rss"},
    ],
    "Business": [
        {"url": "https://feeds.bbci.co.uk/news/business/rss.xml", "type": "rss"},
        {"url": "https://www.cnbc.com/id/10001147/device/rss/rss.html", "type": "rss"},
    ],
    "Science": [
        {"url": "https://www.scientificamerican.com/feed/", "type": "rss"},
        {"url": "https://phys.org/rss-feed/", "type": "rss"},
    ],
    "Health": [
        {"url": "https://feeds.bbci.co.uk/news/health/rss.xml", "type": "rss"},
        {"url": "https://www.medicalnewstoday.com/rss/news.xml", "type": "rss"},
    ],
    "Sports": [
        {"url": "https://feeds.bbci.co.uk/sport/rss.xml", "type": "rss"},
        {"url": "https://www.espn.com/espn/rss/news", "type": "rss"},
    ],
    "Entertainment": [
        {"url": "https://variety.com/feed/", "type": "rss"},
        {"url": "https://deadline.com/feed/", "type": "rss"},
    ],
}

# Simpler fallback URLs that are more likely to work
FALLBACK_ARTICLES = [
    "https://example.com/tech-news",
    "https://example.com/business-news",
    "https://example.com/science-news",
]
