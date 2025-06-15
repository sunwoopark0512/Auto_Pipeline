from types import SimpleNamespace
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import qa_tester as qt


def test_run_step_success(monkeypatch):
    monkeypatch.setitem(sys.modules, "dummy_ok", SimpleNamespace(main=lambda: None))
    res = qt._run_step("dummy_ok")
    assert res.success


def test_run_step_failure(monkeypatch):
    def _boom():
        raise ValueError("bad")

    monkeypatch.setitem(sys.modules, "dummy_fail", SimpleNamespace(main=_boom))
    res = qt._run_step("dummy_fail")
    assert not res.success and "bad" in res.error
