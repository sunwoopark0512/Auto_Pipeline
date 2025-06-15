"""Tests for keyword_auto_pipeline multithreading behavior."""

import importlib
import sys
from types import SimpleNamespace
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class DummyFuture:
    def __init__(self, result):
        self._result = result

    def result(self):
        return self._result


class DummyExecutor:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.submitted = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def submit(self, fn, *args, **kwargs):
        result = fn(*args, **kwargs)
        future = DummyFuture(result)
        self.submitted.append(future)
        return future


def dummy_as_completed(futures):
    for f in futures:
        yield f


def test_max_workers_env(monkeypatch):
    monkeypatch.setenv("MAX_WORKERS", "3")
    dummy_scraper = SimpleNamespace(TwitterSearchScraper=None)
    monkeypatch.setitem(sys.modules, "snscrape", SimpleNamespace(modules=SimpleNamespace(twitter=dummy_scraper)))
    monkeypatch.setitem(sys.modules, "snscrape.modules", SimpleNamespace(twitter=dummy_scraper))
    monkeypatch.setitem(sys.modules, "snscrape.modules.twitter", dummy_scraper)
    import keyword_auto_pipeline as module
    module = importlib.reload(module)

    monkeypatch.setattr(module, "generate_keyword_pairs", lambda x: ["a"])
    monkeypatch.setattr(module, "fetch_google_trends", lambda *a, **k: {})
    monkeypatch.setattr(module, "fetch_twitter_metrics", lambda *a, **k: {})
    monkeypatch.setattr(module, "ThreadPoolExecutor", DummyExecutor)
    monkeypatch.setattr(module, "as_completed", dummy_as_completed)

    module.run_pipeline()
    assert module.MAX_WORKERS == 3


def test_trendreq_per_thread(monkeypatch):
    monkeypatch.setenv("MAX_WORKERS", "4")
    dummy_scraper = SimpleNamespace(TwitterSearchScraper=None)
    monkeypatch.setitem(sys.modules, "snscrape", SimpleNamespace(modules=SimpleNamespace(twitter=dummy_scraper)))
    monkeypatch.setitem(sys.modules, "snscrape.modules", SimpleNamespace(twitter=dummy_scraper))
    monkeypatch.setitem(sys.modules, "snscrape.modules.twitter", dummy_scraper)
    import keyword_auto_pipeline as module
    module = importlib.reload(module)

    instances = []

    class DummyTrendReq:
        def __init__(self, *a, **k):
            instances.append(self)

    monkeypatch.setattr(module, "TrendReq", DummyTrendReq)
    monkeypatch.setattr(module, "generate_keyword_pairs", lambda x: ["a", "b", "c"])
    monkeypatch.setattr(module, "fetch_google_trends", lambda *a, **k: {})
    monkeypatch.setattr(module, "fetch_twitter_metrics", lambda *a, **k: {})
    monkeypatch.setattr(module, "ThreadPoolExecutor", DummyExecutor)
    monkeypatch.setattr(module, "as_completed", dummy_as_completed)

    module.run_pipeline()
    assert len(instances) == 3
