"""
vectordb.py
-----------
Compatible with LangChain 1.1.0

Creates a Chroma vector DB with SentenceTransformer embeddings.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.vectorstores import Chroma
from rag.embedder import get_embedding_model

CHROMA_DIR = "vector_store"


def get_vector_db():
    """
    Initializes (or loads) a ChromaDB instance.
    """

    if not os.path.exists(CHROMA_DIR):
        os.makedirs(CHROMA_DIR)

    embedding = get_embedding_model()

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding,
        collection_name="news_articles"
    )

    return vectordb
