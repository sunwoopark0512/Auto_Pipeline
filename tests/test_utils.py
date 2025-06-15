import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data_flow import batched
from utils.cache_handler import CacheHandler
from utils.input_validator import sanitize_text, parse_json

def test_batched():
    data = [1, 2, 3, 4, 5]
    batches = list(batched(data, batch_size=2))
    assert batches == [(1, 2), (3, 4), (5,)]

def test_cache_handler(tmp_path):
    cache = CacheHandler(directory=tmp_path)
    cache.set("key", {"v": 1}, ttl=1)
    assert cache.get("key") == {"v": 1}


def test_input_validator():
    dirty = "<script>alert(1)</script>{}\n"
    clean = sanitize_text(dirty)
    assert "script" not in clean.lower()
    assert parse_json("{\"a\":1}") == {"a": 1}
    assert parse_json("not json") is None



