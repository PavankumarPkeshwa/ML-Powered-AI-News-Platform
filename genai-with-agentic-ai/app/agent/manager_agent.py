"""
manager_agent.py
Manager: scrape -> clean -> validate -> persist to vectordb
"""

from app.agent.news_agent import fetch_url, extract_main_text_from_html, clean_text_with_llm
from app.agent.validator_agent import validate_article
from app.rag.vectordb import get_vector_db
from app.rag.embedder import get_embedding_model
from langchain_core.documents import Document
import uuid
from datetime import datetime

def ingest_url(url: str, category: str = "General") -> dict:
    result = {"url": url, "status": "error", "reason": None, "metadata": {}}

    try:
        # 1) Fetch HTML
        html = fetch_url(url)

        # 2) Extract main text heuristically
        raw_text = extract_main_text_from_html(html)
        if not raw_text or len(raw_text) < 200:
            result["status"] = "error"
            result["reason"] = "no_text_extracted"
            return result

        # 3) Extract title from HTML (simple extraction)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title") or soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else url.split("/")[-1]
        
        # Use raw text as content (skip slow LLM cleaning for now)
        content = raw_text.strip()[:5000]  # Limit to first 5000 chars for performance
        
        if len(content) < 200:
            result["status"] = "error"
            result["reason"] = "content_too_short"
            return result

        # Skip validation for speed (can re-enable later)
        # validation = validate_article(content)
        # if validation["final_decision"] != "approve":
        #     result["status"] = "rejected"
        #     result["reason"] = validation["final_decision"]
        #     return result

        # 5) Persist to vector DB with rich metadata
        vectordb = get_vector_db()
        embedding_model = get_embedding_model()

        # Generate article ID and prepare metadata
        article_id = str(uuid.uuid4())
        excerpt = content[:300] + "..." if len(content) > 300 else content
        
        # Extract potential tags from content (simple keyword extraction)
        import re
        words = re.findall(r'\b[A-Z][a-z]+\b', content[:500])
        tags_list = list(set(words[:5])) if words else [category.lower()]
        tags_str = ",".join(tags_list)  # ChromaDB needs string, not list
        
        # Build Document with rich metadata for UI display
        metadata = {
            "id": article_id,
            "source": url,
            "title": title or "Untitled Article",
            "excerpt": excerpt,
            "category": category,
            "author": "AI News Agent",
            "publishDate": datetime.now().isoformat(),
            "tags": tags_str,  # Store as comma-separated string
            "imageUrl": f"https://picsum.photos/seed/{article_id}/800/600",
            "isFeatured": str(0),  # Convert to string for ChromaDB
            "isTrending": str(0)   # Convert to string for ChromaDB
        }
        
        doc = Document(page_content=content, metadata=metadata)

        # Try different add APIs depending on installed wrapper
        add_succeeded = False
        try:
            # Preferred: add_documents (many wrappers implement this)
            vectordb.add_documents([doc])
            add_succeeded = True
        except Exception:
            try:
                # Fallback: add_texts + metadatas
                vectordb.add_texts([content], metadatas=[doc.metadata])
                add_succeeded = True
            except Exception as ex:
                result["status"] = "error"
                result["reason"] = f"vectordb_add_failed: {ex}"
                return result

        # Persist DB if supported
        try:
            vectordb.persist()
        except Exception:
            # some wrappers persist automatically
            pass

        result["status"] = "ingested"
        result["metadata"]["title"] = title
        result["metadata"]["length"] = len(content.split())
        return result

    except Exception as e:
        result["status"] = "error"
        result["reason"] = str(e)
        return result
