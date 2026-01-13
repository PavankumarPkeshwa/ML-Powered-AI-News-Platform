"""
langgraph_supervisor.py

Minimal LangGraph-based supervisor that:
- Carries a simple State (user_query, decision, final_answer)
- Implements a Supervisor node that decides whether to trigger scraping
  based on keywords like: latest, today, breaking, refresh
- Wraps existing scraping logic (calls auto_collect_news) without modifying it
- Wraps existing RAG/chat logic (calls chat_message from api.chat_api)
- Connects nodes with conditional edges:
    Supervisor -> Scraper (if scraping needed)
    Supervisor -> RAG (if scraping not needed)
    Scraper -> RAG (always)

Notes:
- This file uses langgraph *if available*. If langgraph is not installed,
  a small internal fallback is used so the module remains testable.
- We DO NOT change existing scraper or RAG functions; they are invoked as-is.

How to use:
    from agents.langgraph_supervisor import run_langgraph
    answer = await run_langgraph("Show me latest technology news")

"""

from dataclasses import dataclass
from typing import Optional
import re
import logging
import asyncio

logger = logging.getLogger(__name__)

# Try to import LangGraph (optional). If unavailable, use a tiny local fallback.
try:
    import langgraph as lg  # type: ignore
    _HAS_LANGGRAPH = True
except Exception:
    lg = None
    _HAS_LANGGRAPH = False

# Import existing functions (we will call them directly)
from agents.supervisor_agent import auto_collect_news
from api.chat_api import ChatMessage, chat_message


@dataclass
class LangState:
    """State carried through the LangGraph.

    - user_query: original user input
    - decision: 'scrape' or 'chat' (set by Supervisor)
    - final_answer: final text returned to user (set by RAG node)
    """
    user_query: str
    decision: Optional[str] = None
    final_answer: Optional[str] = None


# --- Nodes (framework-agnostic wrappers) ---
class SupervisorNode:
    """Supervisor node: decides whether to scrape or call RAG.

    For simplicity, checks for keywords (case-insensitive):
    'latest', 'today', 'breaking', 'refresh'
    If any are present -> decision = 'scrape', else -> 'chat'
    """

    SCRAPE_KEYWORDS = [r"\blatest\b", r"\btoday\b", r"\bbreaking\b", r"\brefresh\b"]

    def run(self, state: LangState) -> LangState:
        message = (state.user_query or "").lower()
        for kw in self.SCRAPE_KEYWORDS:
            if re.search(kw, message):
                state.decision = "scrape"
                logger.info(f"Supervisor decision: SCRAPE (matched '{kw}')")
                return state

        state.decision = "chat"
        logger.info("Supervisor decision: CHAT (no scrape keywords found)")
        return state


class ScraperNode:
    """Scraper node: wraps existing auto_collect_news function.

    - Calls auto_collect_news(quick_mode=True, clear_old=False) by default
    - Does not modify any existing scraping code
    - Sets state.final_answer with a short summary
    """

    def __init__(self, quick_mode: bool = True, clear_old: bool = False):
        self.quick_mode = quick_mode
        self.clear_old = clear_old

    async def run(self, state: LangState) -> LangState:
        logger.info("ScraperNode: triggering auto_collect_news()")
        try:
            stats = await auto_collect_news(quick_mode=self.quick_mode, clear_old=self.clear_old)
            total = sum(stats.values()) if isinstance(stats, dict) else 0
            state.final_answer = f"Scraping completed: {total} articles collected. Proceeding to answer your query."
            logger.info(state.final_answer)
            return state
        except Exception as e:
            state.final_answer = f"Scraper error: {e}"
            logger.error("ScraperNode encountered an error", exc_info=True)
            return state


class RAGNode:
    """RAG node: wraps your existing chat/message handler.

    - Uses the same interface as /chat/message endpoint by calling chat_message
      with a ChatMessage and returns text from the ChatResponse.
    - This keeps existing RAG logic untouched and reuses existing formatting.
    """

    async def run(self, state: LangState) -> LangState:
        logger.info("RAGNode: invoking chat_message(...) to produce final answer")
        try:
            # chat_message is synchronous (FastAPI style); call in threadpool if needed
            loop = asyncio.get_event_loop()

            # Wrap chat_message to run in executor to avoid blocking event loop
            def _call_chat():
                cm = ChatMessage(message=state.user_query)
                resp = chat_message(cm)
                return resp

            resp = await loop.run_in_executor(None, _call_chat)

            state.final_answer = getattr(resp, "response", str(resp))
            logger.info("RAGNode: final answer ready")
            return state
        except Exception as e:
            state.final_answer = f"RAG node error: {e}"
            logger.error("RAGNode encountered an error", exc_info=True)
            return state


# --- Small Graph Runner (framework-agnostic) ---
async def run_langgraph(user_query: str) -> str:
    """Execute the minimal LangGraph flow with conditional edges.

    Flow logic (simple and explicit):
      1. Supervisor decides
      2a. If decision == 'scrape': run Scraper, then run RAG
      2b. If decision == 'chat': run RAG directly

    Returns: final_answer string
    """
    state = LangState(user_query=user_query)

    # Supervisor
    sup = SupervisorNode()
    state = sup.run(state)

    # Conditional routing
    if state.decision == "scrape":
        scraper = ScraperNode(quick_mode=True, clear_old=False)
        state = await scraper.run(state)
        # Always follow up with RAG to answer user's query
        rag = RAGNode()
        state = await rag.run(state)
    else:
        rag = RAGNode()
        state = await rag.run(state)

    # Ensure we return a string
    return state.final_answer or "No answer produced"


# Optional: If langgraph is installed, expose a thin wrapper that builds a LangGraph
# graph using the library's constructs. This is informational and non-blocking.
# It does NOT change the behavior of run_langgraph above.
if _HAS_LANGGRAPH:
    # Attempt to create a LangGraph graph (best-effort). The exact API may differ
    # across LangGraph versions; this is a minimal example showing intent.
    try:
        # This demonstrates how one might register nodes and conditional edges
        # using an imagined LangGraph API. If the user's environment has a
        # different API, this block can be adapted.
        Graph = lg.Graph
        Node = lg.Node

        # Build nodes (callable wrappers)
        def _sup_fn(payload: dict):
            s = LangState(user_query=payload.get("user_query"))
            s = SupervisorNode().run(s)
            return s.__dict__

        async def _scrape_fn(payload: dict):
            s = LangState(**payload)
            s = await ScraperNode().run(s)
            return s.__dict__

        async def _rag_fn(payload: dict):
            s = LangState(**payload)
            s = await RAGNode().run(s)
            return s.__dict__

        try:
            lg_graph = Graph("news_supervisor")
            lg_graph.add_node(Node(id="supervisor", func=_sup_fn))
            lg_graph.add_node(Node(id="scraper", func=_scrape_fn))
            lg_graph.add_node(Node(id="rag", func=_rag_fn))

            # Conditional edges (pseudocode/illustrative):
            # supervisor -> scraper [if decision == 'scrape']
            # supervisor -> rag [if decision == 'chat']
            # scraper -> rag [always]
            # Note: adapt to actual LangGraph API in your environment
        except Exception:
            logger.debug("Could not auto-build LangGraph graph; this is optional")
    except Exception:
        logger.debug("LangGraph integration skipped: incompatible API")
else:
    logger.info("LangGraph not installed - using minimal internal runner (run_langgraph)")
