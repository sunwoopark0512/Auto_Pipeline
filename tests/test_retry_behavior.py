from unittest.mock import MagicMock
import types
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import hook_generator
import notion_hook_uploader


def test_get_gpt_response_retries(monkeypatch):
    attempts = {"count": 0}

    def fake_create(*args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise Exception("temporary failure")
        mock_resp = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message = {"content": "ok"}
        mock_resp.choices = [mock_choice]
        return mock_resp

    monkeypatch.setattr(hook_generator, "openai", types.SimpleNamespace(ChatCompletion=types.SimpleNamespace(create=fake_create)))

    result = hook_generator.get_gpt_response("test")
    assert result == "ok"
    assert attempts["count"] == 3


def test_page_exists_retries(monkeypatch):
    attempts = {"count": 0}

    def fake_query(*args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise Exception("temporary failure")
        return {"results": [1]}

    monkeypatch.setattr(notion_hook_uploader.notion.databases, "query", fake_query)
    assert notion_hook_uploader.page_exists("keyword") is True
    assert attempts["count"] == 3
