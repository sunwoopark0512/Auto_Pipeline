import importlib
import json
import types
import sys
import time

import pytest


def setup_module(module):
    # create dummy notion_client before import
    dummy = types.ModuleType('notion_client')
    class DummyPages:
        def create(self, *args, **kwargs):
            pass
    class DummyClient:
        def __init__(self, auth=None):
            self.pages = DummyPages()
    dummy.Client = DummyClient
    sys.modules['notion_client'] = dummy
    sys.modules.setdefault('dotenv', types.SimpleNamespace(load_dotenv=lambda: None))


def import_module(monkeypatch, tmp_path):
    monkeypatch.setenv('NOTION_API_TOKEN', 'x')
    monkeypatch.setenv('NOTION_HOOK_DB_ID', 'y')
    failed_path = tmp_path / 'failed.json'
    monkeypatch.setenv('REPARSED_OUTPUT_PATH', str(failed_path))
    module = importlib.reload(importlib.import_module('retry_failed_uploads'))
    return module, failed_path


def test_retry_failed_uploads(monkeypatch, tmp_path):
    module, path = import_module(monkeypatch, tmp_path)

    items = [
        {'keyword': 'a'},
        {'keyword': 'b'},
    ]
    def mock_load():
        return items
    calls = []
    def mock_create(item):
        calls.append(item['keyword'])
        if item['keyword'] == 'a':
            raise Exception('boom')
    monkeypatch.setattr(module, 'load_failed_items', mock_load)
    monkeypatch.setattr(module, 'create_retry_page', mock_create)
    monkeypatch.setattr(time, 'sleep', lambda x: None)

    module.retry_failed_uploads()

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data[0]['keyword'] == 'a'
    assert 'retry_error' in data[0]
    assert calls == ['a', 'b']
