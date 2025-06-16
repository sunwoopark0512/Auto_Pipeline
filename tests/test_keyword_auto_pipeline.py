import sys
import types

# Stub heavy external dependencies
sys.modules['pytrends'] = types.ModuleType('pytrends')
request_mod = types.ModuleType('pytrends.request')
request_mod.TrendReq = object
sys.modules['pytrends.request'] = request_mod

sys.modules['snscrape'] = types.ModuleType('snscrape')
mods = types.ModuleType('snscrape.modules')
sys.modules['snscrape.modules'] = mods
sys.modules['snscrape.modules.twitter'] = types.ModuleType('snscrape.modules.twitter')

sys.path.insert(0, '.')
sys.path.insert(0, 'Auto_Pipeline')

import keyword_auto_pipeline as kap


def test_filter_keywords():
    entries = [
        {
            'keyword': 'g1',
            'source': 'GoogleTrends',
            'score': kap.GOOGLE_TRENDS_MIN_SCORE,
            'growth': kap.GOOGLE_TRENDS_MIN_GROWTH,
            'cpc': kap.MIN_CPC,
        },
        {
            'keyword': 'g2',
            'source': 'GoogleTrends',
            'score': kap.GOOGLE_TRENDS_MIN_SCORE - 1,
            'growth': kap.GOOGLE_TRENDS_MIN_GROWTH,
            'cpc': kap.MIN_CPC,
        },
        {
            'keyword': 't1',
            'source': 'Twitter',
            'mentions': kap.TWITTER_MIN_MENTIONS,
            'top_retweet': kap.TWITTER_MIN_TOP_RETWEET,
            'cpc': kap.MIN_CPC,
        },
        {
            'keyword': 't2',
            'source': 'Twitter',
            'mentions': kap.TWITTER_MIN_MENTIONS - 1,
            'top_retweet': kap.TWITTER_MIN_TOP_RETWEET,
            'cpc': kap.MIN_CPC,
        },
    ]
    filtered = kap.filter_keywords(entries)
    names = {e['keyword'] for e in filtered}
    assert names == {'g1', 't1'}
