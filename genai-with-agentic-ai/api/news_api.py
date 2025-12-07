from fastapi import APIRouter, Query
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.vectordb import get_vector_db
from rag.rag_chain import get_rag_chain
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/fetch")
def fetch_news(
    category: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Fetch news articles from the vector database.
    Returns structured articles for the frontend.
    """
    try:
        vectordb = get_vector_db()
        
        # Get all documents from the collection
        collection = vectordb._collection
        results = collection.get(include=["metadatas", "documents"])
        
        # Extract documents and metadatas
        all_docs = results.get("documents", [])
        all_metadatas = results.get("metadatas", [])
        
        # Filter by category if provided
        filtered_articles = []
        for i, (doc_content, metadata) in enumerate(zip(all_docs, all_metadatas)):
            if category and metadata.get("category") != category:
                continue
                
            article_id = metadata.get("id", str(uuid.uuid4()))
            title = metadata.get("title", doc_content[:100] + "...")
            excerpt = doc_content[:300] + "..." if len(doc_content) > 300 else doc_content
            
            # Handle tags - convert from string if needed
            tags_data = metadata.get("tags", [])
            if isinstance(tags_data, str):
                tags = tags_data.split(",") if tags_data else []
            else:
                tags = tags_data if tags_data else []
            
            article = {
                "id": article_id,
                "_id": article_id,
                "title": title,
                "excerpt": metadata.get("excerpt", excerpt),
                "content": doc_content,
                "imageUrl": metadata.get("imageUrl", f"https://picsum.photos/seed/{article_id}/800/600"),
                "author": metadata.get("author", "AI News Agent"),
                "publishDate": metadata.get("publishDate", datetime.now().isoformat()),
                "readTime": estimate_read_time(doc_content),
                "category": metadata.get("category", "General"),
                "tags": tags,
                "source": metadata.get("source", "https://news.example.com"),
                "isFeatured": metadata.get("isFeatured", 0),
                "isTrending": metadata.get("isTrending", 0)
            }
            filtered_articles.append(article)
        
        # Apply offset and limit
        paginated_articles = filtered_articles[offset:offset + limit]
        
        return paginated_articles
    
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc(), "articles": []}


@router.get("/featured")
def get_featured_article():
    """
    Get a featured article (first article from the database)
    """
    try:
        vectordb = get_vector_db()
        collection = vectordb._collection
        results = collection.get(include=["metadatas", "documents"], limit=1)
        
        docs = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        
        if not docs:
            return {"error": "No articles found"}
        
        content = docs[0]
        metadata = metadatas[0]
        
        title = metadata.get("title", content[:100] + "...")
        article_id = metadata.get("id", str(uuid.uuid4()))
        
        article = {
            "id": article_id,
            "_id": article_id,
            "title": title,
            "excerpt": content[:300] + "..." if len(content) > 300 else content,
            "content": content,
            "imageUrl": metadata.get("imageUrl", f"https://picsum.photos/seed/{article_id}/800/600"),
            "author": metadata.get("author", "AI News Agent"),
            "publishDate": metadata.get("publishDate", datetime.now().isoformat()),
            "readTime": estimate_read_time(content),
            "category": metadata.get("category", "General"),
            "tags": metadata.get("tags", []),
            "source": metadata.get("source", ""),
            "isFeatured": 1,
            "isTrending": 0
        }
        
        return article
    
    except Exception as e:
        return {"error": str(e)}


@router.get("/trending")
def get_trending_articles(limit: int = Query(3, ge=1, le=10)):
    """
    Get trending articles (most recent articles)
    """
    try:
        vectordb = get_vector_db()
        collection = vectordb._collection
        results = collection.get(include=["metadatas", "documents"], limit=limit)
        
        docs = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        
        articles = []
        for content, metadata in zip(docs, metadatas):
            title = metadata.get("title", content[:100] + "...")
            article_id = metadata.get("id", str(uuid.uuid4()))
            
            article = {
                "id": article_id,
                "_id": article_id,
                "title": title,
                "excerpt": content[:300] + "..." if len(content) > 300 else content,
                "content": content,
                "imageUrl": metadata.get("imageUrl", f"https://picsum.photos/seed/{article_id}/800/600"),
                "author": metadata.get("author", "AI News Agent"),
                "publishDate": metadata.get("publishDate", datetime.now().isoformat()),
                "readTime": estimate_read_time(content),
                "category": metadata.get("category", "General"),
                "tags": metadata.get("tags", []),
                "source": metadata.get("source", ""),
                "isFeatured": 0,
                "isTrending": 1
            }
            articles.append(article)
        
        return articles
    
    except Exception as e:
        return {"error": str(e), "articles": []}


@router.get("/search")
def search_articles(q: str = Query(..., min_length=1)):
    """
    Search articles using semantic search
    """
    try:
        vectordb = get_vector_db()
        docs = vectordb.similarity_search(q, k=20)
        
        articles = []
        for doc in docs:
            metadata = doc.metadata
            content = doc.page_content
            
            title = metadata.get("title", content[:100] + "...")
            article_id = metadata.get("id", str(uuid.uuid4()))
            
            article = {
                "id": article_id,
                "_id": article_id,
                "title": title,
                "excerpt": content[:200] + "...",
                "content": content,
                "imageUrl": metadata.get("imageUrl", f"https://picsum.photos/seed/{article_id}/800/600"),
                "author": metadata.get("author", "AI News Agent"),
                "publishDate": metadata.get("publishDate", datetime.now().isoformat()),
                "readTime": estimate_read_time(content),
                "category": infer_category(content, title),
                "tags": extract_tags(content),
                "source": metadata.get("source", "")
            }
            articles.append(article)
        
        return articles
    
    except Exception as e:
        return {"error": str(e), "articles": []}


# Helper functions
def estimate_read_time(content: str) -> int:
    """Estimate reading time in minutes (200 words per minute)"""
    words = len(content.split())
    minutes = max(1, words // 200)
    return minutes


def infer_category(content: str, title: str) -> str:
    """Infer category from content keywords"""
    text = (title + " " + content).lower()
    
    if any(word in text for word in ["tech", "technology", "software", "ai", "artificial intelligence", "computer"]):
        return "Technology"
    elif any(word in text for word in ["business", "market", "economy", "finance", "stock", "company"]):
        return "Business"
    elif any(word in text for word in ["health", "medical", "disease", "doctor", "hospital", "medicine"]):
        return "Health"
    elif any(word in text for word in ["science", "research", "study", "scientist", "discovery"]):
        return "Science"
    elif any(word in text for word in ["sport", "game", "player", "team", "championship", "football", "basketball"]):
        return "Sports"
    elif any(word in text for word in ["entertainment", "movie", "music", "celebrity", "film", "actor"]):
        return "Entertainment"
    else:
        return "General"


def extract_tags(content: str) -> List[str]:
    """Extract relevant tags from content"""
    # Simple keyword extraction - can be enhanced with NLP
    common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    
    words = content.lower().split()
    word_freq = {}
    
    for word in words:
        word = word.strip(".,!?;:")
        if len(word) > 4 and word not in common_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top 5 words
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    tags = [word for word, _ in sorted_words[:5]]
    
    return tags if tags else ["news", "latest"]
