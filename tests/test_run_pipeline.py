import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import run_pipeline


def test_pipeline_sequence_no_missing_scripts():
    assert "parse_failed_gpt.py" not in run_pipeline.PIPELINE_SEQUENCE
    assert "notify_retry_result.py" not in run_pipeline.PIPELINE_SEQUENCE


def test_run_pipeline_calls_run_script(monkeypatch):
    called = []

    def fake_run_script(script):
        called.append(script)
        return True

    monkeypatch.setattr(run_pipeline, "run_script", fake_run_script)
    run_pipeline.run_pipeline()
    assert called == run_pipeline.PIPELINE_SEQUENCE
