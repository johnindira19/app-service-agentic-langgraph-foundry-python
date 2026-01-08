import pytest
from src.agents.langgraph_task_agent import get_time_func, LangGraphTaskAgent


def test_get_time_valid_timezone():
    s = get_time_func("Asia/Kolkata")
    assert "IST" in s or "+0530" in s


def test_get_time_invalid_timezone():
    s = get_time_func("Invalid/Timezone")
    assert s.startswith("Failed to get time for Invalid/Timezone:")


def test_extract_assistant_text_from_dict():
    agent = LangGraphTaskAgent.__new__(LangGraphTaskAgent)
    # Create a fake result structure with message dicts
    result = {
        "messages": [
            {"type": "user", "content": "Hello"},
            {"type": "ai", "content": "This is the answer"}
        ]
    }

    text = agent._extract_assistant_text(result)
    assert text == "This is the answer"
