from fastapi import APIRouter, Query
import sys
sys.path.insert(0, '/workspaces/ML-Powered-AI-News-Platform/genai-with-agentic-ai')
from agents.supervisor_agent import ingest_url
from agents.langgraph_supervisor import run_langgraph

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.get("/ingest")
def ingest(url: str = Query(...)):
    return ingest_url(url)

@router.post("/langgraph/run")
async def langgraph_run(query: str = Query(...)):
    """Run the LangGraph supervisor for a user query.

    If the supervisor decides a scrape is needed, it will run the scraper
    and then the RAG responder; otherwise, it will call RAG directly.

    Returns: {"answer": str}
    """
    answer = await run_langgraph(query)
    return {"answer": answer}
