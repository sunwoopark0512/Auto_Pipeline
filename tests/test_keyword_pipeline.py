import json
import os
import sys
import types
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

pytrends_module = types.ModuleType("pytrends")
pytrends_request_module = types.ModuleType("pytrends.request")

class DummyTrendReq:
    def __init__(self, *args, **kwargs):
        pass

pytrends_request_module.TrendReq = DummyTrendReq
pytrends_module.request = pytrends_request_module
sys.modules["pytrends"] = pytrends_module
sys.modules["pytrends.request"] = pytrends_request_module

snscrape_module = types.ModuleType("snscrape")
snscrape_modules_module = types.ModuleType("snscrape.modules")
snscrape_twitter_module = types.ModuleType("snscrape.modules.twitter")

class DummyScraper:
    def __init__(self, *args, **kwargs):
        pass

    def get_items(self):
        return []

snscrape_twitter_module.TwitterSearchScraper = DummyScraper
snscrape_modules_module.twitter = snscrape_twitter_module
snscrape_module.modules = snscrape_modules_module
sys.modules["snscrape"] = snscrape_module
sys.modules["snscrape.modules"] = snscrape_modules_module
sys.modules["snscrape.modules.twitter"] = snscrape_twitter_module

import keyword_auto_pipeline as kap


def test_generate_keyword_pairs_basic():
    details = {"t1": ["a", "b"], "t2": ["x"]}
    result = kap.generate_keyword_pairs(details)
    assert set(result) == {"t1 a", "t1 b", "t2 x"}


def test_generate_keyword_pairs_empty():
    assert kap.generate_keyword_pairs({}) == []


def test_filter_keywords_empty():
    assert kap.filter_keywords([]) == []


def test_filter_keywords_google_and_twitter():
    entries = [
        {"keyword": "k", "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1500},
        {"keyword": "k", "source": "GoogleTrends", "score": 50, "growth": 1.5, "cpc": 1500},
        {"keyword": "k", "source": "Twitter", "mentions": 100, "top_retweet": 60, "cpc": 1500},
        {"keyword": "k", "source": "Twitter", "mentions": 10, "top_retweet": 60, "cpc": 1500},
    ]
    filtered = kap.filter_keywords(entries)
    assert entries[0] in filtered
    assert entries[2] in filtered
    assert len(filtered) == 2


def test_filter_keywords_duplicates_preserved():
    entry = {"keyword": "k", "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1500}
    filtered = kap.filter_keywords([entry, entry])
    assert filtered == [entry, entry]


def test_run_pipeline_empty_keywords(tmp_path, monkeypatch):
    output = tmp_path / "out.json"
    monkeypatch.setattr(kap, "OUTPUT_PATH", str(output))

    with mock.patch.object(kap, "generate_keyword_pairs", return_value=[]), \
         mock.patch.object(kap, "TrendReq"):
        kap.run_pipeline()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["filtered_keywords"] == []


def test_run_pipeline_with_duplicates(tmp_path, monkeypatch):
    output = tmp_path / "out.json"
    monkeypatch.setattr(kap, "OUTPUT_PATH", str(output))

    keywords = ["kw1", "kw1"]
    google_data = {"keyword": "kw1", "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1500}
    twitter_data = {"keyword": "kw1", "source": "Twitter", "mentions": 100, "top_retweet": 60, "cpc": 1500}

    with mock.patch.object(kap, "generate_keyword_pairs", return_value=keywords), \
         mock.patch.object(kap, "fetch_google_trends", return_value=google_data), \
         mock.patch.object(kap, "fetch_twitter_metrics", return_value=twitter_data), \
         mock.patch.object(kap, "TrendReq"):
        kap.run_pipeline()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data["filtered_keywords"]) == 4
    for item in data["filtered_keywords"]:
        assert item in (google_data, twitter_data)
