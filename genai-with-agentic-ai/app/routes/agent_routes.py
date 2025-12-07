from fastapi import APIRouter, Query
import sys
sys.path.insert(0, '/workspaces/ML-Powered-AI-News-Platform/genai-with-agentic-ai')
from agents.supervisor_agent import ingest_url

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.get("/ingest")
def ingest(url: str = Query(...)):
    return ingest_url(url)
