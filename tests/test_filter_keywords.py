import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import types

dummy_pt = types.ModuleType('pytrends')
dummy_pt.__path__ = []
request_mod = types.ModuleType('pytrends.request')
request_mod.TrendReq = lambda *a, **k: None
sys.modules.setdefault('pytrends', dummy_pt)
sys.modules.setdefault('pytrends.request', request_mod)

dummy_sn = types.ModuleType('snscrape.modules.twitter')
sys.modules.setdefault('snscrape', types.ModuleType('snscrape'))
sys.modules.setdefault('snscrape.modules', types.ModuleType('snscrape.modules'))
sys.modules.setdefault('snscrape.modules.twitter', dummy_sn)

import keyword_auto_pipeline as kap


def test_filter_keywords():
    entries = [
        {
            'keyword': 'a',
            'source': 'GoogleTrends',
            'score': kap.GOOGLE_TRENDS_MIN_SCORE + 10,
            'growth': kap.GOOGLE_TRENDS_MIN_GROWTH + 0.5,
            'cpc': kap.MIN_CPC + 100
        },
        {
            'keyword': 'b',
            'source': 'GoogleTrends',
            'score': kap.GOOGLE_TRENDS_MIN_SCORE - 5,
            'growth': kap.GOOGLE_TRENDS_MIN_GROWTH + 0.5,
            'cpc': kap.MIN_CPC + 100
        },
        {
            'keyword': 'c',
            'source': 'Twitter',
            'mentions': kap.TWITTER_MIN_MENTIONS + 5,
            'top_retweet': kap.TWITTER_MIN_TOP_RETWEET + 1,
            'cpc': kap.MIN_CPC + 100
        },
        {
            'keyword': 'd',
            'source': 'Twitter',
            'mentions': kap.TWITTER_MIN_MENTIONS - 1,
            'top_retweet': kap.TWITTER_MIN_TOP_RETWEET + 1,
            'cpc': kap.MIN_CPC + 100
        },
    ]

    result = kap.filter_keywords(entries)
    assert entries[0] in result
    assert entries[2] in result
    assert entries[1] not in result
    assert entries[3] not in result
