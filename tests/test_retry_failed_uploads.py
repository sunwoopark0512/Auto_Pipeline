import sys
import os
import json
from pathlib import Path
from types import SimpleNamespace
import importlib

sys.modules['dotenv'] = SimpleNamespace(load_dotenv=lambda: None)
sys.modules['notion_client'] = SimpleNamespace(Client=lambda **k: 'client')

os.environ['NOTION_API_TOKEN'] = 'x'
os.environ['NOTION_HOOK_DB_ID'] = 'y'


def import_retry_module(tmp_path):
    os.environ['REPARSED_OUTPUT_PATH'] = str(tmp_path / 'failed.json')
    if 'retry_failed_uploads' in sys.modules:
        del sys.modules['retry_failed_uploads']
    import retry_failed_uploads
    return retry_failed_uploads


def test_retry_logic(tmp_path, monkeypatch):
    module = import_retry_module(tmp_path)
    items = [{'keyword': 'k1'}, {'keyword': 'k2'}]
    monkeypatch.setattr(module, 'load_failed_items', lambda: items)

    calls = []
    def mock_create(item):
        calls.append(item)
        if item['keyword'] == 'k1':
            raise Exception('fail')
    monkeypatch.setattr(module, 'create_retry_page', mock_create)
    monkeypatch.setattr(module.time, 'sleep', lambda x: None)

    module.retry_failed_uploads()

    out = json.loads(Path(module.FAILED_PATH).read_text())
    assert out[0]['keyword'] == 'k1'
    assert out[0]['retry_error'] == 'fail'
    assert len(calls) == 2
