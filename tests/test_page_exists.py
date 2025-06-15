import importlib
import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest


def _setup_module(module_name, monkeypatch):
    dummy_nc = types.ModuleType('notion_client')
    class DummyClient:
        def __init__(self, *a, **kw):
            pass
    dummy_nc.Client = DummyClient
    monkeypatch.setitem(sys.modules, 'notion_client', dummy_nc)

    dummy_dotenv = types.ModuleType('dotenv')
    dummy_dotenv.load_dotenv = lambda *a, **kw: None
    monkeypatch.setitem(sys.modules, 'dotenv', dummy_dotenv)

    os.makedirs('logs', exist_ok=True)

    module = importlib.import_module(module_name)
    return module


def test_page_exists_hook(monkeypatch):
    mod = _setup_module('notion_hook_uploader', monkeypatch)
    class DummyDB:
        def query(self, database_id, filter, page_size):
            if filter['title']['equals'] == 'exist':
                return {'results': [1]}
            return {'results': []}
    mod.notion = types.SimpleNamespace(databases=DummyDB())
    mod.NOTION_HOOK_DB_ID = 'db'

    assert mod.page_exists('exist') is True
    assert mod.page_exists('none') is False


def test_page_exists_keywords(monkeypatch):
    mod = _setup_module('scripts.notion_uploader', monkeypatch)
    class DummyDB:
        def query(self, database_id, filter, page_size):
            if filter['title']['equals'] == 'exist':
                return {'results': [1]}
            return {'results': []}
    mod.notion = types.SimpleNamespace(databases=DummyDB())
    mod.NOTION_DB_ID = 'db'
    mod.uploaded_cache = set()

    assert mod.page_exists('exist') is True
    assert mod.page_exists('none') is False
    mod.uploaded_cache.add('cached')
    assert mod.page_exists('cached') is True
