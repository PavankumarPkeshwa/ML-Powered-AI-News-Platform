"""
embedder.py
-----------
Loads embedding model used to convert text → vectors.

We use a FREE HuggingFace Model:
- all-MiniLM-L6-v2  (small, fast, accurate)
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# Cache the embedding model to avoid reloading
_embedding_model_cache = None

def get_embedding_model():
    """
    Returns a FREE encoder model that can embed text chunks.
    Uses caching to avoid PyTorch device issues.
    """
    global _embedding_model_cache
    
    if _embedding_model_cache is not None:
        return _embedding_model_cache
    
    try:
        # Set environment variable to avoid meta tensor issues
        os.environ['TRANSFORMERS_OFFLINE'] = '0'
        
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        _embedding_model_cache = embedding_model
        return embedding_model
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        # Fallback: try without device specification
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        _embedding_model_cache = embedding_model
        return embedding_model
