from unittest import mock
import os
import sys
import types

import pytest

# Create dummy modules for optional dependencies
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sys.modules.setdefault('pytrends', types.ModuleType('pytrends'))
request_mod = types.ModuleType('pytrends.request')
setattr(request_mod, 'TrendReq', object)
sys.modules['pytrends.request'] = request_mod

sys.modules.setdefault('snscrape', types.ModuleType('snscrape'))
sys.modules.setdefault('snscrape.modules', types.ModuleType('snscrape.modules'))
sys.modules['snscrape.modules.twitter'] = types.ModuleType('snscrape.modules.twitter')

import keyword_auto_pipeline as kap


def test_fetch_cpc_caches_value():
    with mock.patch('keyword_auto_pipeline.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'cpc': 1500}
        mock_get.return_value.raise_for_status.return_value = None

        first = kap.fetch_cpc('test')
        second = kap.fetch_cpc('test')

        assert first == 1500
        assert second == 1500
        mock_get.assert_called_once()


def test_select_top_keywords_uses_cpc_sorting():
    entries = [
        {'keyword': 'a', 'cpc': 1000},
        {'keyword': 'b', 'cpc': 2000},
        {'keyword': 'c', 'cpc': 1500},
    ]
    top = kap.select_top_keywords(entries, top_n=2)
    assert [e['keyword'] for e in top] == ['b', 'c']

