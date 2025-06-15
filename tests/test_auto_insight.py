import types
from unittest.mock import MagicMock

import auto_insight as ai

class DummyResponse:
    def __init__(self, data):
        self.data = data

class DummyTable:
    def __init__(self, data):
        self._data = data
    def select(self, *args, **kwargs):
        return self
    def execute(self):
        return DummyResponse(self._data)

class DummySupabase:
    def __init__(self, data):
        self._data = data
    def table(self, name):
        assert name == ai.INSIGHT_TABLE
        return DummyTable(self._data)

class DummyNotion:
    def __init__(self):
        self.pages = MagicMock()

def test_fetch_insights():
    data = [{"id": 1, "summary": "a"}]
    client = DummySupabase(data)
    result = ai.fetch_insights(client)
    assert result == data

def test_create_notion_page(monkeypatch):
    notion = DummyNotion()
    monkeypatch.setattr(ai, "NOTION_INSIGHT_DB_ID", "db")
    ai.create_notion_page({"id": 1, "summary": "hello"}, notion)
    notion.pages.create.assert_called_once()
    props = notion.pages.create.call_args[1]["properties"]
    assert props["요약"]["title"][0]["text"]["content"] == "hello"

def test_upload_insights(monkeypatch):
    notion = DummyNotion()
    monkeypatch.setattr(ai, "NOTION_INSIGHT_DB_ID", "db")
    records = [{"id": 1, "summary": "x"}, {"id": 2, "summary": "y"}]
    ai.upload_insights(records, notion)
    assert notion.pages.create.call_count == 2
