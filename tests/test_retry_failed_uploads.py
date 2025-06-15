import json
import importlib.util
from pathlib import Path
import sys
import types

import pytest


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setattr('time.sleep', lambda *_args, **_kwargs: None)
    # Provide a dummy notion_client for tests
    dummy = types.ModuleType("notion_client")
    class DummyPages:
        def create(self, **_):
            pass

    class DummyClient:
        def __init__(self, auth=None):
            self.pages = DummyPages()

    dummy.Client = DummyClient
    monkeypatch.setitem(sys.modules, "notion_client", dummy)
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda *_, **__: None
    monkeypatch.setitem(sys.modules, "dotenv", dotenv)
    monkeypatch.setenv("NOTION_API_TOKEN", "t")
    monkeypatch.setenv("NOTION_HOOK_DB_ID", "d")


def setup_file(tmp_path, data):
    file_path = tmp_path / "failed.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False))
    return file_path


def test_retry_success(tmp_path, monkeypatch):
    data = [{
        "keyword": "topic1 test1",
        "parsed": {
            "hook_lines": ["a", "b"],
            "blog_paragraphs": ["p1", "p2", "p3"],
            "video_titles": ["v1", "v2"]
        }
    }]
    file_path = setup_file(tmp_path, data)
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(file_path))
    spec = importlib.util.spec_from_file_location(
        "retry_failed_uploads", Path("scripts/retry_failed_uploads.py")
    )
    retry_failed_uploads = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(retry_failed_uploads)
    calls = []
    monkeypatch.setattr(retry_failed_uploads, "RETRY_DELAY", 0)
    monkeypatch.setattr(retry_failed_uploads.notion.pages, "create", lambda **_: calls.append(1))
    retry_failed_uploads.retry_failed_uploads()
    assert len(calls) == 1
    assert json.loads(file_path.read_text()) == data


def test_retry_failure(tmp_path, monkeypatch):
    data = [{
        "keyword": "topic2 test2",
        "parsed": {
            "hook_lines": ["a", "b"],
            "blog_paragraphs": ["p1", "p2", "p3"],
            "video_titles": ["v1", "v2"]
        }
    }]
    file_path = setup_file(tmp_path, data)
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(file_path))
    spec = importlib.util.spec_from_file_location(
        "retry_failed_uploads", Path("scripts/retry_failed_uploads.py")
    )
    retry_failed_uploads = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(retry_failed_uploads)
    def raise_error(**_):
        raise RuntimeError("fail")
    monkeypatch.setattr(retry_failed_uploads, "RETRY_DELAY", 0)
    monkeypatch.setattr(retry_failed_uploads.notion.pages, "create", raise_error)
    retry_failed_uploads.retry_failed_uploads()
    result = json.loads(file_path.read_text())
    assert result[0]["retry_error"] == "fail"
