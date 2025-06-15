import os
import sys
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import super_orchestrator as so


def test_generate_keywords():
    assert so.generate_keywords("topic") == ["topic idea 1", "topic idea 2"]


def test_pipeline_runs(monkeypatch):
    calls = []

    def fake_record(*args, **kwargs):
        calls.append((args, kwargs))

    monkeypatch.setattr(so, "record_content", fake_record)
    monkeypatch.setattr(so, "upload_to_wordpress", lambda **kwargs: ("ok", 1))
    monkeypatch.setattr(so, "send_slack_message", lambda *a, **k: None)

    # avoid actual DB commit and connection close
    monkeypatch.setattr(so, "conn", mock.MagicMock())

    so.run_pipeline("test")
    assert calls
