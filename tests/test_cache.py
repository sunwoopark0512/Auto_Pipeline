import os
from autopipe.cache import KeywordCache


def test_keyword_cache(tmp_path):
    path = tmp_path / "cache.json"
    cache = KeywordCache(str(path))
    assert not cache.exists("foo")
    cache.add("foo")
    assert cache.exists("foo")
    # reload to ensure persistence
    cache2 = KeywordCache(str(path))
    assert cache2.exists("foo")
