import os
import sys
import types
import importlib

# Stub external modules before importing targets
pytrends = types.ModuleType("pytrends")
request_mod = types.ModuleType("pytrends.request")
class DummyTrendReq:
    def __init__(self, *args, **kwargs):
        pass
request_mod.TrendReq = DummyTrendReq
pytrends.request = request_mod
sys.modules['pytrends'] = pytrends
sys.modules['pytrends.request'] = request_mod

sns_mod = types.ModuleType("snscrape.modules.twitter")
sns_mod.TwitterSearchScraper = lambda *a, **k: iter([])
sys.modules['snscrape'] = types.ModuleType('snscrape')
sys.modules['snscrape.modules'] = types.ModuleType('snscrape.modules')
sys.modules['snscrape.modules.twitter'] = sns_mod

import keyword_auto_pipeline


def test_generate_keyword_pairs():
    data = {"A": ["1", "2"], "B": ["x"]}
    assert keyword_auto_pipeline.generate_keyword_pairs(data) == ["A 1", "A 2", "B x"]


def test_parse_generated_text(monkeypatch):
    os.makedirs('logs', exist_ok=True)
    dummy_nc = types.ModuleType('notion_client')
    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass
    dummy_nc.Client = DummyClient
    monkeypatch.setitem(sys.modules, 'notion_client', dummy_nc)

    dummy_dotenv = types.ModuleType('dotenv')
    dummy_dotenv.load_dotenv = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, 'dotenv', dummy_dotenv)

    nhu = importlib.import_module('notion_hook_uploader')
    text = (
        "후킹 문장1: Line1\n"
        "후킹 문장2: Line2\n"
        "블로그 초안:\n"
        "Para1\n"
        "Para2\n"
        "Para3\n"
        "영상 제목:\n"
        "- Title1\n"
        "- Title2\n"
    )
    result = nhu.parse_generated_text(text)
    assert result["hook_lines"] == ["Line1", "Line2"]
    assert result["blog_paragraphs"] == ["Para1"]
    assert result["video_titles"] == ["Title2"]
