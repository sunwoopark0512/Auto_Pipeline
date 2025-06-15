import run_pipeline


def test_run_pipeline_skips_missing(monkeypatch):
    calls = []

    def dummy_run_script(script):
        calls.append(script)
        if script == "missing.py":
            return False
        return True

    monkeypatch.setattr(run_pipeline, "run_script", dummy_run_script)
    monkeypatch.setattr(
        run_pipeline,
        "PIPELINE_SEQUENCE",
        ["first.py", "missing.py", "last.py"],
    )

    run_pipeline.run_pipeline()

    assert calls == ["first.py", "missing.py", "last.py"]
