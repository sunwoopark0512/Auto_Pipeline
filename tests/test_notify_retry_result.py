import json
import importlib
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_notify_retry_result_success(tmp_path, monkeypatch):
    path = tmp_path / "reparsed.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump([], f)
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(path))
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://example.com/webhook")
    with mock.patch("scripts.notify_retry_result.requests.post") as post:
        module = importlib.import_module("scripts.notify_retry_result")
        importlib.reload(module)
        module.notify_retry_result()
        post.assert_called_once()
        args, kwargs = post.call_args
        assert kwargs["json"]["text"].startswith("✅")


def test_notify_retry_result_failures(tmp_path, monkeypatch):
    path = tmp_path / "reparsed.json"
    data = [
        {"keyword": "kw1"},
        {"keyword": "kw2"}
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    monkeypatch.setenv("REPARSED_OUTPUT_PATH", str(path))
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "http://example.com/webhook")
    with mock.patch("scripts.notify_retry_result.requests.post") as post:
        module = importlib.import_module("scripts.notify_retry_result")
        importlib.reload(module)
        module.notify_retry_result()
        post.assert_called_once()
        text = post.call_args[1]["json"]["text"]
        assert "2개" in text and "kw1" in text
