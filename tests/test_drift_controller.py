import importlib
from unittest.mock import MagicMock

import ai_self_heal.drift_controller as drift_controller


def test_fetch_drift_success(monkeypatch):
    class Resp:
        def __init__(self):
            self.status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {"value": 0.5}

    monkeypatch.setattr(drift_controller.requests, "get", lambda *a, **k: Resp())
    assert drift_controller.fetch_drift() == 0.5


def test_fetch_drift_failure(monkeypatch):
    def raise_error(*args, **kwargs):
        raise drift_controller.requests.RequestException()

    monkeypatch.setattr(drift_controller.requests, "get", raise_error)
    assert drift_controller.fetch_drift() is None


def test_handle_drift(monkeypatch):
    called = []

    def run(cmd, check=False):
        called.append(cmd)
        return 0

    monkeypatch.setattr(drift_controller.subprocess, "run", run)
    drift_controller.handle_drift(0.4)
    assert [c[0] for c in called] == ["python", "python"]
