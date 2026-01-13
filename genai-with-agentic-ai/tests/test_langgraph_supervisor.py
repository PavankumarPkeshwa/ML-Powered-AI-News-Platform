import asyncio
from agents.langgraph_supervisor import SupervisorNode, run_langgraph, LangState


def test_supervisor_detects_scrape():
    sup = SupervisorNode()
    s = LangState(user_query="Show me the latest technology news")
    s = sup.run(s)
    assert s.decision == "scrape"


def test_supervisor_detects_chat():
    sup = SupervisorNode()
    s = LangState(user_query="Will AI replace human jobs in the next 5 years?")
    s = sup.run(s)
    assert s.decision == "chat"


def test_run_langgraph_routes_and_handles_scrape(monkeypatch):
    # Monkeypatch auto_collect_news to avoid network calls
    async def fake_auto_collect_news(quick_mode=True, clear_old=False):
        return {"Technology": 2}

    class FakeResp:
        def __init__(self, text):
            self.response = text

    def fake_chat_message(cm):
        return FakeResp("This is a fake chat response based on current DB")

    monkeypatch.setattr("agents.langgraph_supervisor.auto_collect_news", fake_auto_collect_news)
    monkeypatch.setattr("agents.langgraph_supervisor.chat_message", fake_chat_message)

    loop = asyncio.get_event_loop()
    answer = loop.run_until_complete(run_langgraph("latest tech news"))

    assert isinstance(answer, str)
    assert "Scraping completed" in answer or "fake chat response" in answer
