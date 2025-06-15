import subprocess
import run_pipeline


def test_run_script_success(tmp_path, monkeypatch):
    script = tmp_path / "dummy.py"
    script.write_text("print('ok')\n")
    monkeypatch.setattr(run_pipeline.os.path, "join", lambda a, b: str(script))
    assert run_pipeline.run_script("dummy.py")


def test_run_script_failure(monkeypatch):
    monkeypatch.setattr(run_pipeline.os.path, "join", lambda a, b: "nonexistent.py")
    assert not run_pipeline.run_script("missing.py")


def test_run_pipeline_sequence(monkeypatch):
    called = []
    monkeypatch.setattr(run_pipeline, "PIPELINE_SEQUENCE", ["a.py", "b.py"])
    def fake_run_script(name):
        called.append(name)
        return True
    monkeypatch.setattr(run_pipeline, "run_script", fake_run_script)
    run_pipeline.run_pipeline()
    assert called == ["a.py", "b.py"]

