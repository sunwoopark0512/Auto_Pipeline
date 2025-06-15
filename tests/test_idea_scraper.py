import os
import sys
import types
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import idea_scraper


class DummyResponse:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data


def test_generate_hooks_from_keywords():
    hooks = idea_scraper.generate_hooks_from_keywords(['테스트'])
    assert hooks == [
        '테스트 때문에 모두가 놀랐다!?',
        '당신도 테스트 하고 있나요?',
        '지금 테스트 안 하면 손해입니다.'
    ]


def test_fetch_youtube_autocomplete(monkeypatch):
    def dummy_get(url, headers):
        return DummyResponse([None, ['a', 'b', 'c']])

    monkeypatch.setattr(idea_scraper.requests, 'get', dummy_get)
    assert idea_scraper.fetch_youtube_autocomplete('kw') == ['a', 'b', 'c']


def test_fetch_google_trends(monkeypatch):
    class DummyTrendReq:
        def __init__(self, hl='ko', tz=540):
            pass

        def build_payload(self, *args, **kwargs):
            pass
        def related_queries(self):
            return {"kw": {"top": pd.DataFrame({"query": ["x", "y"]})}}

    dummy_module = types.SimpleNamespace(TrendReq=DummyTrendReq)
    monkeypatch.setitem(sys.modules, 'pytrends.request', dummy_module)

    result = idea_scraper.fetch_google_trends('kw')
    assert result == ['x', 'y']
