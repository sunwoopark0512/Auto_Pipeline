import sys
import types
import logging
import pytest

@pytest.fixture(autouse=True)
def patch_external_modules(monkeypatch):
    # Patch modules not installed in test environment
    monkeypatch.setitem(sys.modules, 'dotenv', types.SimpleNamespace(load_dotenv=lambda: None))
    monkeypatch.setitem(sys.modules, 'notion_client', types.SimpleNamespace(Client=lambda *a, **kw: None))

    sns = types.ModuleType('snscrape')
    sns.modules = types.ModuleType('snscrape.modules')
    sns.modules.twitter = types.ModuleType('snscrape.modules.twitter')
    monkeypatch.setitem(sys.modules, 'snscrape', sns)
    monkeypatch.setitem(sys.modules, 'snscrape.modules', sns.modules)
    monkeypatch.setitem(sys.modules, 'snscrape.modules.twitter', sns.modules.twitter)

    pytrends = types.ModuleType('pytrends.request')
    pytrends.TrendReq = lambda *a, **kw: None
    monkeypatch.setitem(sys.modules, 'pytrends.request', pytrends)

    monkeypatch.setattr(logging, 'FileHandler', lambda *a, **kw: logging.NullHandler())

