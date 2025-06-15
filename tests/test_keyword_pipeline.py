import json
import sys
import types

# Provide dummy modules for optional dependencies
sys.modules.setdefault('pytrends', types.ModuleType('pytrends'))
request_mod = types.ModuleType('request')
setattr(request_mod, 'TrendReq', lambda *args, **kwargs: None)
sys.modules['pytrends.request'] = request_mod
sns_module = types.ModuleType('snscrape')
modules_mod = types.ModuleType('modules')
twitter_mod = types.ModuleType('twitter')
modules_mod.twitter = twitter_mod
sns_module.modules = modules_mod
sys.modules['snscrape'] = sns_module
sys.modules['snscrape.modules'] = modules_mod
sys.modules['snscrape.modules.twitter'] = twitter_mod

import keyword_auto_pipeline


def test_generate_keyword_pairs():
    details = {"Topic1": ["a", "b"], "Topic2": ["x"]}
    pairs = keyword_auto_pipeline.generate_keyword_pairs(details)
    assert set(pairs) == {"Topic1 a", "Topic1 b", "Topic2 x"}


def test_fetch_cpc_dummy_caching():
    first = keyword_auto_pipeline.fetch_cpc_dummy("kw1")
    second = keyword_auto_pipeline.fetch_cpc_dummy("kw1")
    assert first == second
    assert 500 <= first <= 2000


def test_filter_keywords():
    entries = [
        {"keyword": "k1", "source": "GoogleTrends", "score": 70, "growth": 1.4, "cpc": 1000},
        {"keyword": "k2", "source": "GoogleTrends", "score": 50, "growth": 1.4, "cpc": 1000},
        {"keyword": "t1", "source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": 1500},
        {"keyword": "t2", "source": "Twitter", "mentions": 10, "top_retweet": 5, "cpc": 1000},
    ]
    filtered = keyword_auto_pipeline.filter_keywords(entries)
    assert {"keyword": "k1", "source": "GoogleTrends", "score": 70, "growth": 1.4, "cpc": 1000} in filtered
    assert {"keyword": "t1", "source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": 1500} in filtered
    assert len(filtered) == 2


def test_collect_data_for_keyword(monkeypatch):
    def fake_gtrend(keyword, pytrends):
        return {"keyword": keyword, "source": "GoogleTrends", "score": 70, "growth": 1.4, "cpc": 1000}

    def fake_twitter(keyword, max_tweets=100):
        return {"keyword": keyword, "source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": 1500}

    monkeypatch.setattr(keyword_auto_pipeline, "fetch_google_trends", fake_gtrend)
    monkeypatch.setattr(keyword_auto_pipeline, "fetch_twitter_metrics", fake_twitter)

    result = keyword_auto_pipeline.collect_data_for_keyword("kw", None)
    assert len(result) == 2
    assert result[0]["source"] == "GoogleTrends"
    assert result[1]["source"] == "Twitter"


def test_run_pipeline_integration(monkeypatch, tmp_path):
    def fake_generate_keyword_pairs(details):
        return ["Topic1 a"]

    def fake_collect(keyword, pytrends):
        return [
            {"keyword": keyword, "source": "GoogleTrends", "score": 70, "growth": 1.4, "cpc": 1000},
            {"keyword": keyword, "source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": 1500},
        ]

    class DummyTrendReq:
        def __init__(self, *args, **kwargs):
            pass

    monkeypatch.setattr(keyword_auto_pipeline, "generate_keyword_pairs", fake_generate_keyword_pairs)
    monkeypatch.setattr(keyword_auto_pipeline, "collect_data_for_keyword", fake_collect)
    monkeypatch.setattr(keyword_auto_pipeline, "TrendReq", DummyTrendReq)

    output = tmp_path / "out.json"
    monkeypatch.setattr(keyword_auto_pipeline, "OUTPUT_PATH", str(output))
    keyword_auto_pipeline.run_pipeline()

    with open(output) as f:
        data = json.load(f)
    assert data["filtered_keywords"][0]["keyword"] == "Topic1 a"

