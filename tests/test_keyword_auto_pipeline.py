import sys
import types

# Stub external dependencies used during module import
pytrends_request = types.ModuleType('pytrends.request')
pytrends_request.TrendReq = lambda *a, **k: None
pytrends = types.ModuleType('pytrends')
pytrends.request = pytrends_request
sys.modules['pytrends'] = pytrends
sys.modules['pytrends.request'] = pytrends_request
sys.modules['snscrape'] = types.ModuleType('snscrape')
sys.modules['snscrape.modules'] = types.ModuleType('snscrape.modules')
sys.modules['snscrape.modules.twitter'] = types.ModuleType('snscrape.modules.twitter')

import keyword_auto_pipeline as kap


def test_generate_keyword_pairs():
    topic_details = {'A': ['x', 'y'], 'B': ['z']}
    pairs = kap.generate_keyword_pairs(topic_details)
    assert set(pairs) == {'A x', 'A y', 'B z'}
    assert len(pairs) == 3


def test_filter_keywords():
    entries = [
        {
            'keyword': 'g1',
            'source': 'GoogleTrends',
            'score': kap.GOOGLE_TRENDS_MIN_SCORE + 1,
            'growth': kap.GOOGLE_TRENDS_MIN_GROWTH + 0.1,
            'cpc': kap.MIN_CPC + 10,
        },
        {
            'keyword': 'g2',
            'source': 'GoogleTrends',
            'score': kap.GOOGLE_TRENDS_MIN_SCORE - 1,
            'growth': kap.GOOGLE_TRENDS_MIN_GROWTH + 0.1,
            'cpc': kap.MIN_CPC + 10,
        },
        {
            'keyword': 't1',
            'source': 'Twitter',
            'mentions': kap.TWITTER_MIN_MENTIONS + 1,
            'top_retweet': kap.TWITTER_MIN_TOP_RETWEET + 1,
            'cpc': kap.MIN_CPC + 10,
        },
        {
            'keyword': 't2',
            'source': 'Twitter',
            'mentions': kap.TWITTER_MIN_MENTIONS - 1,
            'top_retweet': kap.TWITTER_MIN_TOP_RETWEET + 1,
            'cpc': kap.MIN_CPC + 10,
        },
    ]
    filtered = kap.filter_keywords(entries)
    keywords = {item['keyword'] for item in filtered}
    assert keywords == {'g1', 't1'}
