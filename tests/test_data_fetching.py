import types
import sys
import os
import importlib

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Stub modules required for import
pytrends_mod = types.ModuleType('pytrends')
request_mod = types.ModuleType('pytrends.request')
class DummyTrendReq:
    pass
request_mod.TrendReq = DummyTrendReq
pytrends_mod.request = request_mod
sys.modules['pytrends'] = pytrends_mod
sys.modules['pytrends.request'] = request_mod

sns_pkg = types.ModuleType('snscrape')
modules_pkg = types.ModuleType('snscrape.modules')
sns_mod = types.ModuleType('snscrape.modules.twitter')
modules_pkg.twitter = sns_mod
sns_pkg.modules = modules_pkg
sys.modules['snscrape'] = sns_pkg
sys.modules['snscrape.modules'] = modules_pkg
sys.modules['snscrape.modules.twitter'] = sns_mod

import keyword_auto_pipeline as kap

class DummySeries:
    def __init__(self, data):
        self.data = list(data)
    def __getitem__(self, item):
        if isinstance(item, slice):
            return DummySeries(self.data[item])
        return self.data[item]
    def mean(self):
        return sum(self.data) / len(self.data)

class DummyDataFrame:
    def __init__(self, keyword, data):
        self.keyword = keyword
        self.data = DummySeries(data)
        self.empty = False
    def __contains__(self, item):
        return item == self.keyword
    def __getitem__(self, item):
        return self.data

class DummyTrends:
    def build_payload(self, *args, **kwargs):
        pass
    def interest_over_time(self):
        return DummyDataFrame('test', [10, 20, 30, 40, 50, 60, 70])

def test_fetch_google_trends(monkeypatch):
    monkeypatch.setattr(kap, 'fetch_cpc_dummy', lambda kw: 999)
    result = kap.fetch_google_trends('test', DummyTrends())
    assert result['keyword'] == 'test'
    assert result['source'] == 'GoogleTrends'
    assert result['score'] == int((50 + 60 + 70) / 3)
    assert result['cpc'] == 999

def test_fetch_twitter_metrics(monkeypatch):
    class DummyTweet:
        def __init__(self, count):
            self.retweetCount = count
    class DummyScraper:
        def __init__(self, query):
            self.query = query
        def get_items(self):
            return iter([DummyTweet(1), DummyTweet(5), DummyTweet(10)])
    sns_mod.TwitterSearchScraper = DummyScraper
    import importlib
    importlib.reload(kap)
    monkeypatch.setattr(kap, 'fetch_cpc_dummy', lambda kw: 123)
    result = kap.fetch_twitter_metrics('kw', max_tweets=3)
    assert result['keyword'] == 'kw'
    assert result['source'] == 'Twitter'
    assert result['mentions'] == 3
    assert result['top_retweet'] == 10
    assert result['cpc'] == 123
