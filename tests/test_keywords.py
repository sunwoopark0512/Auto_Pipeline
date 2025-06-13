import builtins
from keyword_auto_pipeline import generate_keyword_pairs, filter_keywords


def test_generate_keyword_pairs():
    data = {"A": ["a1", "a2"]}
    assert generate_keyword_pairs(data) == ["A a1", "A a2"]


def test_filter_keywords():
    entries = [
        {"keyword": "A", "source": "GoogleTrends", "score": 70, "growth": 1.5, "cpc": 1500},
        {"keyword": "B", "source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": 1200},
        {"keyword": "C", "source": "GoogleTrends", "score": 50, "growth": 1.5, "cpc": 1500},
        {"keyword": "D", "source": "Twitter", "mentions": 20, "top_retweet": 60, "cpc": 1200},
    ]
    filtered = filter_keywords(entries)
    assert entries[0] in filtered
    assert entries[1] in filtered
    assert entries[2] not in filtered
    assert entries[3] not in filtered
