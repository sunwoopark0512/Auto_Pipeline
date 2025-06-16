import pytest
import random
import sys
import os
import types

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.makedirs("logs", exist_ok=True)

# Provide dummy third-party modules for import
sys.modules.setdefault("pytrends", types.ModuleType("pytrends"))
sys.modules.setdefault("pytrends.request", types.ModuleType("request"))
setattr(sys.modules["pytrends.request"], "TrendReq", object)

snscrape_mod = types.ModuleType("snscrape")
modules_mod = types.ModuleType("modules")
twitter_mod = types.ModuleType("twitter")
modules_mod.twitter = twitter_mod
snscrape_mod.modules = modules_mod
sys.modules.setdefault("snscrape", snscrape_mod)
sys.modules.setdefault("snscrape.modules", modules_mod)
sys.modules.setdefault("snscrape.modules.twitter", twitter_mod)

sys.modules.setdefault("notion_client", types.ModuleType("notion_client"))
client_class = type("Client", (), {"__init__": lambda self, *a, **k: None})
sys.modules["notion_client"].Client = client_class

sys.modules.setdefault("dotenv", types.ModuleType("dotenv"))
sys.modules["dotenv"].load_dotenv = lambda *a, **k: None

sys.modules.setdefault("openai", types.ModuleType("openai"))
sys.modules["openai"].ChatCompletion = type("ChatCompletion", (), {"create": lambda *a, **k: None})

from keyword_auto_pipeline import generate_keyword_pairs, fetch_cpc_dummy, cpc_cache, filter_keywords
from notion_hook_uploader import parse_generated_text, truncate_text
from hook_generator import generate_hook_prompt


def test_generate_keyword_pairs():
    details = {"Topic": ["Sub1", "Sub2"], "Other": ["A"]}
    pairs = generate_keyword_pairs(details)
    assert pairs == ["Topic Sub1", "Topic Sub2", "Other A"]


def test_fetch_cpc_dummy_caching(monkeypatch):
    cpc_cache.clear()
    calls = []
    def fake_randint(a, b):
        calls.append(1)
        return 1500
    monkeypatch.setattr(random, "randint", fake_randint)
    first = fetch_cpc_dummy("kw")
    second = fetch_cpc_dummy("kw")
    assert first == 1500
    assert second == 1500
    assert len(calls) == 1


def test_filter_keywords():
    entries = [
        {"keyword": "g1", "source": "GoogleTrends", "score": 70, "growth": 1.5, "cpc": 1200},
        {"keyword": "g2", "source": "GoogleTrends", "score": 50, "growth": 1.5, "cpc": 1200},
        {"keyword": "t1", "source": "Twitter", "mentions": 40, "top_retweet": 70, "cpc": 1500},
        {"keyword": "t2", "source": "Twitter", "mentions": 20, "top_retweet": 70, "cpc": 1500},
        {"keyword": "t3", "source": "Twitter", "mentions": 40, "top_retweet": 40, "cpc": 1500},
        {"keyword": "g3", "source": "GoogleTrends", "score": 70, "growth": 1.5, "cpc": 800},
    ]
    filtered = filter_keywords(entries)
    keywords = {e["keyword"] for e in filtered}
    assert keywords == {"g1", "t1"}


def test_parse_generated_text():
    text = (
        "후킹 문장1: 첫번째\n"
        "후킹 문장2: 두번째\n"
        "블로그 초안:\n첫 단락.\n둘째 단락.\n셋째 단락.\n"
        "영상 제목:\n- 제목1\n- 제목2\n"
    )
    parsed = parse_generated_text(text)
    assert parsed["hook_lines"] == ["첫번째", "두번째"]
    assert parsed["blog_paragraphs"] == ["첫 단락."]
    assert parsed["video_titles"] == ["제목2"]


def test_truncate_text():
    text = "a" * 25
    assert truncate_text(text, max_length=10) == "a" * 10


def test_generate_hook_prompt():
    prompt = generate_hook_prompt("키워드", "토픽", "Google", 10, 1.2, 5)
    assert "키워드" in prompt
    assert "Google" in prompt

