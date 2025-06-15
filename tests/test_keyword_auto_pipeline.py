import keyword_auto_pipeline as kap

def test_generate_keyword_pairs_count():
    pairs = kap.generate_keyword_pairs(kap.TOPIC_DETAILS)
    assert len(pairs) == len(kap.TOPIC_DETAILS) * 3

def test_filter_keywords():
    entries = [
        {"source": "GoogleTrends", "score": 70, "growth": 1.5, "cpc": 1500},
        {"source": "GoogleTrends", "score": 50, "growth": 1.5, "cpc": 1500},
        {"source": "Twitter", "mentions": 40, "top_retweet": 60, "cpc": 1500},
        {"source": "Twitter", "mentions": 20, "top_retweet": 60, "cpc": 1500},
    ]
    filtered = kap.filter_keywords(entries)
    assert len(filtered) == 2
