"""
news_agent.py
Scraper + LLM-based cleaner with RSS feed support and article discovery.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import feedparser
from urllib.parse import urljoin, urlparse
import logging

# use local LLM (no API token required)
from langchain_core.prompts import PromptTemplate
from app.utils.local_llm import LocalLLM

logger = logging.getLogger(__name__)

def _get_llm():
    """
    Returns a local HuggingFace LLM.
    Model is downloaded and cached locally (no API token needed).
    """
    return LocalLLM(model_name="google/flan-t5-base", max_length=512)

def fetch_url(url: str, timeout: int = 10) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GenAI-Scraper/1.0; +https://example.com/bot)"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def parse_rss_feed(feed_url: str, limit: int = 10) -> List[str]:
    """
    Parse RSS feed and extract article URLs.
    Returns list of article URLs.
    """
    try:
        feed = feedparser.parse(feed_url)
        article_urls = []
        
        for entry in feed.entries[:limit]:
            if hasattr(entry, 'link'):
                article_urls.append(entry.link)
        
        logger.info(f"📰 Found {len(article_urls)} articles from RSS feed")
        return article_urls
    except Exception as e:
        logger.error(f"❌ RSS parsing error: {str(e)}")
        return []


def discover_article_links(homepage_url: str, limit: int = 10) -> List[str]:
    """
    Discover article links from a homepage.
    Returns list of article URLs.
    """
    try:
        html = fetch_url(homepage_url)
        soup = BeautifulSoup(html, "html.parser")
        
        article_urls = set()
        base_domain = urlparse(homepage_url).netloc
        
        # Common article link patterns
        selectors = [
            'article a[href]',
            'a.article-link',
            'a.post-link',
            'a[href*="/article/"]',
            'a[href*="/story/"]',
            'a[href*="/news/"]',
            'a[href*="/post/"]',
            'h2 a[href]',
            'h3 a[href]',
            '.story a[href]',
            '.article a[href]',
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    # Make absolute URL
                    full_url = urljoin(homepage_url, href)
                    
                    # Filter: same domain, looks like article (has path)
                    parsed = urlparse(full_url)
                    if parsed.netloc == base_domain and len(parsed.path) > 1:
                        # Exclude common non-article pages
                        excluded = ['/tag/', '/category/', '/author/', '/page/', 
                                  '/search/', '/login', '/signup', '/about', 
                                  '/contact', '/privacy', '/terms']
                        if not any(ex in full_url.lower() for ex in excluded):
                            article_urls.add(full_url)
                    
                    if len(article_urls) >= limit:
                        break
            
            if len(article_urls) >= limit:
                break
        
        result = list(article_urls)[:limit]
        logger.info(f"📰 Discovered {len(result)} article links from {homepage_url}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Article discovery error: {str(e)}")
        return []

def extract_main_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Try <article>
    article = soup.find("article")
    if article:
        text = article.get_text(separator="\n", strip=True)
        if len(text) > 200:
            return text

    # Fallback: all <p>
    paragraphs = soup.find_all("p")
    if paragraphs:
        pts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        if pts:
            return "\n\n".join(pts)

    # fallback to body text
    body = soup.body
    return body.get_text(separator="\n", strip=True) if body else ""

def _call_llm(llm, prompt_text: str) -> str:
    """
    Defensive LLM caller: use .invoke if available, else call as function.
    Returns string output.
    """
    try:
        # new-style: llm.invoke
        return llm.invoke(prompt_text)
    except Exception:
        try:
            return llm(prompt_text)
        except Exception:
            # Last fallback: if llm has run or generate methods (very rare), try them
            try:
                return llm.run(prompt_text)
            except Exception:
                return ""  # fail safe

def clean_text_with_llm(raw_text: str) -> dict:
    llm = _get_llm()

    prompt = PromptTemplate(
        input_variables=["raw"],
        template=(
            "You are a helpful text-cleaner. Input is raw extracted news HTML text that may contain nav, ads,"
            " captions, timestamps, and broken sentences. Produce a clean output with two fields:\n\n"
            "TITLE: <a concise title or empty if none>\n\n"
            "CONTENT: <cleaned article content, full sentences, no ads, no 'read more' fragments>\n\n"
            "Only output the TITLE and CONTENT blocks (no extra commentary).\n\nRAW:\n\n{raw}\n\n"
            "CLEAN OUTPUT:"
        )
    )

    prompt_text = prompt.format(raw=raw_text)
    raw_resp = _call_llm(llm, prompt_text) or ""

    title = ""
    content = raw_resp.strip()

    # parse "TITLE:" and "CONTENT:" if model respected format
    if "TITLE:" in raw_resp and "CONTENT:" in raw_resp:
        try:
            after_title = raw_resp.split("TITLE:", 1)[1]
            title_part, content_part = after_title.split("CONTENT:", 1)
            title = title_part.strip().splitlines()[0].strip()
            content = content_part.strip()
        except Exception:
            content = raw_resp.strip()

    return {"title": title, "content": content}
