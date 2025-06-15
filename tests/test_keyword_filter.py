import importlib
import os
import sys

from types import SimpleNamespace

# Create dummy modules so importing keyword_auto_pipeline does not require
# external dependencies.
sys.modules.setdefault('pytrends', SimpleNamespace(request=SimpleNamespace(TrendReq=object)))
sys.modules.setdefault('pytrends.request', SimpleNamespace(TrendReq=object))
sys.modules.setdefault('snscrape', SimpleNamespace(modules=SimpleNamespace(twitter=SimpleNamespace())))
sys.modules.setdefault('snscrape.modules', SimpleNamespace(twitter=SimpleNamespace()))
sys.modules.setdefault('snscrape.modules.twitter', SimpleNamespace())

import keyword_auto_pipeline as kap


def reload_module():
    return importlib.reload(sys.modules['keyword_auto_pipeline'])


def test_filter_keywords_default(monkeypatch):
    monkeypatch.delenv('GOOGLE_TRENDS_MIN_SCORE', raising=False)
    monkeypatch.delenv('GOOGLE_TRENDS_MIN_GROWTH', raising=False)
    monkeypatch.delenv('TWITTER_MIN_MENTIONS', raising=False)
    monkeypatch.delenv('TWITTER_MIN_TOP_RETWEET', raising=False)
    monkeypatch.delenv('MIN_CPC', raising=False)
    mod = reload_module()
    entries = [
        {'source': 'GoogleTrends', 'score': 60, 'growth': 1.3, 'cpc': 1000},
        {'source': 'Twitter', 'mentions': 30, 'top_retweet': 50, 'cpc': 1000},
    ]
    filtered = mod.filter_keywords(entries)
    assert len(filtered) == 2


def test_filter_keywords_env(monkeypatch):
    monkeypatch.setenv('GOOGLE_TRENDS_MIN_SCORE', '70')
    monkeypatch.setenv('GOOGLE_TRENDS_MIN_GROWTH', '1.5')
    monkeypatch.setenv('TWITTER_MIN_MENTIONS', '40')
    monkeypatch.setenv('TWITTER_MIN_TOP_RETWEET', '100')
    monkeypatch.setenv('MIN_CPC', '1500')
    mod = reload_module()
    entries = [
        {'source': 'GoogleTrends', 'score': 80, 'growth': 1.6, 'cpc': 1600},
        {'source': 'Twitter', 'mentions': 50, 'top_retweet': 200, 'cpc': 1700},
        {'source': 'GoogleTrends', 'score': 60, 'growth': 1.4, 'cpc': 1600},
    ]
    filtered = mod.filter_keywords(entries)
    assert len(filtered) == 2
