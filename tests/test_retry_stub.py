from scripts.retry import run


def test_retry_success(monkeypatch):
    import subprocess

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: type("Res", (object,), {"returncode": 0})(),
    )
    assert run(["echo", "ok"], retries=2) == 0
