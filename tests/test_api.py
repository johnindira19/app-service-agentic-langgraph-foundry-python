from fastapi.testclient import TestClient
import pytest

from importlib import import_module
app_module = import_module('src.app')
from src.models import ChatMessage, Role

client = TestClient(app_module.app)

@pytest.fixture(autouse=True)
def mock_langgraph(monkeypatch):
    async def fake_process(message: str, session_id: str = None):
        return ChatMessage(role=Role.ASSISTANT, content=f"Echo: {message}")

    # Replace the async process_message method on the current agent instance
    monkeypatch.setattr(app_module.app_instance.langgraph_agent, "process_message", fake_process)
    yield


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "langgraph_initialized" in body


def test_chat_langgraph():
    r = client.post("/api/chat/langgraph", json={"message": "hello", "sessionId": "s1"})
    assert r.status_code == 200
    body = r.json()
    assert body["role"] == "assistant"
    assert "Echo: hello" in body["content"]
