import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from types import SimpleNamespace
import importlib
import notion_hook_uploader as uploader

class DummyDB:
    def __init__(self, results):
        self._results = results
    def query(self, database_id, filter, page_size):
        return {"results": self._results}

class DummyClient:
    def __init__(self, results):
        self.databases = DummyDB(results)

def test_page_exists_true(monkeypatch):
    monkeypatch.setattr(uploader, "notion", DummyClient([1]))
    assert uploader.page_exists("kw") is True

def test_page_exists_false(monkeypatch):
    monkeypatch.setattr(uploader, "notion", DummyClient([]))
    assert uploader.page_exists("kw") is False
