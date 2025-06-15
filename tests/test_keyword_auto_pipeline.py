import types
import sys
import importlib
import os

# Ensure project root is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Mock external dependencies before importing the module
pytrends = types.ModuleType('pytrends')
pytrends.request = types.ModuleType('pytrends.request')
pytrends.request.TrendReq = object
sys.modules['pytrends'] = pytrends
sys.modules['pytrends.request'] = pytrends.request

snscrape = types.ModuleType('snscrape')
snscrape.modules = types.ModuleType('snscrape.modules')
snscrape.modules.twitter = types.ModuleType('snscrape.modules.twitter')
sys.modules['snscrape'] = snscrape
sys.modules['snscrape.modules'] = snscrape.modules
sys.modules['snscrape.modules.twitter'] = snscrape.modules.twitter

keyword_module = importlib.import_module('keyword_auto_pipeline')
generate_keyword_pairs = keyword_module.generate_keyword_pairs


def test_generate_keyword_pairs_basic():
    topics = {
        "Topic1": ["sub1", "sub2"],
        "Topic2": ["a"]
    }
    result = generate_keyword_pairs(topics)
    assert result == ["Topic1 sub1", "Topic1 sub2", "Topic2 a"]

