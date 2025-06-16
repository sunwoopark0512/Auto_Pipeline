import sys
import types

# Stub pytrends.request.TrendReq before importing module
pytrends_module = types.ModuleType('pytrends')
request_submodule = types.ModuleType('request')
request_submodule.TrendReq = lambda *a, **k: None
pytrends_module.request = request_submodule
sys.modules['pytrends'] = pytrends_module
sys.modules['pytrends.request'] = request_submodule

# Stub snscrape.modules.twitter
snscrape_mod = types.ModuleType('snscrape')
modules_mod = types.ModuleType('modules')
twitter_mod = types.ModuleType('twitter')
modules_mod.twitter = twitter_mod
snscrape_mod.modules = modules_mod
sys.modules['snscrape'] = snscrape_mod
sys.modules['snscrape.modules'] = modules_mod
sys.modules['snscrape.modules.twitter'] = twitter_mod

import keyword_auto_pipeline


def test_generate_keyword_pairs():
    pairs = keyword_auto_pipeline.generate_keyword_pairs({'A': ['x', 'y'], 'B': ['z']})
    assert pairs == ['A x', 'A y', 'B z']
