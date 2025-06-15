import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from types import SimpleNamespace

import run_pipeline as rp


def test_unknown_step_validation(monkeypatch):
    cfg = SimpleNamespace(PIPELINE_ORDER=["no_such_module"])
    monkeypatch.setattr("run_pipeline._load_config", lambda p: cfg)
    try:
        rp.run_pipeline("dummy")
    except ValueError as exc:
        assert "Unknown step" in str(exc)


def test_pipeline_collects_failures(monkeypatch):
    ok_mod = SimpleNamespace(main=lambda: None)
    bad_mod = SimpleNamespace(main=lambda: 1 / 0)

    def _import(name):
        if name == "good":
            return ok_mod
        if name == "bad":
            return bad_mod
        raise ModuleNotFoundError

    cfg = SimpleNamespace(PIPELINE_ORDER=["good", "bad"], NOTIFIER_STEP=None)
    monkeypatch.setattr("importlib.import_module", _import)
    monkeypatch.setattr("run_pipeline._load_config", lambda p: cfg)
    code = rp.run_pipeline("cfg")
    assert code == 1
