import json
import importlib

import pytest


def setup_module(module):
    # ensure environment variables so module import does not exit
    import os
    os.environ.setdefault('NOTION_API_TOKEN', 'x')
    os.environ.setdefault('NOTION_HOOK_DB_ID', 'y')


def test_retry_logic(tmp_path, monkeypatch):
    path = tmp_path / 'failed.json'
    items = [
        {'keyword': 'a'},
        {'keyword': 'b'},
        {'keyword': 'c'},
    ]
    path.write_text(json.dumps(items), encoding='utf-8')
    monkeypatch.setenv('REPARSED_OUTPUT_PATH', str(path))

    module = importlib.reload(importlib.import_module('retry_failed_uploads'))

    def fake_create_retry_page(item):
        if item['keyword'] == 'b':
            raise Exception('boom')

    monkeypatch.setattr(module, 'create_retry_page', fake_create_retry_page)
    monkeypatch.setattr(module, 'RETRY_DELAY', 0)

    module.retry_failed_uploads()

    data = json.loads(path.read_text(encoding='utf-8'))
    assert len(data) == 1
    assert data[0]['keyword'] == 'b'
