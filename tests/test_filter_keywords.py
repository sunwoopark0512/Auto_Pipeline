import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import keyword_auto_pipeline as kap


def test_filter_keywords_skips_missing_cpc():
    entries = [
        {"keyword": "test1", "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": None},
        {"keyword": "test2", "source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": None},
    ]
    assert kap.filter_keywords(entries) == []


def test_filter_keywords_handles_none_fields():
    entries = [
        {"keyword": "kw", "source": "GoogleTrends", "score": None, "growth": None, "cpc": 1500},
        {"keyword": "tw", "source": "Twitter", "mentions": None, "top_retweet": None, "cpc": 1500},
    ]
    result = kap.filter_keywords(entries)
    assert len(result) == 0


def test_filter_keywords_valid():
    entries = [
        {"keyword": "kw", "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1500},
        {"keyword": "tw", "source": "Twitter", "mentions": 35, "top_retweet": 60, "cpc": 1500},
    ]
    result = kap.filter_keywords(entries)
    assert len(result) == 2
