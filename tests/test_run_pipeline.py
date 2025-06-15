import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import run_pipeline

EXPECTED_SEQUENCE = [
    "hook_generator.py",
    "retry_failed_uploads.py",
    "retry_dashboard_notifier.py",
]

def test_pipeline_sequence():
    assert run_pipeline.PIPELINE_SEQUENCE == EXPECTED_SEQUENCE

def test_run_pipeline_calls_scripts_in_order(monkeypatch):
    called = []

    def fake_run_script(script):
        called.append(script)
        return True

    monkeypatch.setattr(run_pipeline, "run_script", fake_run_script)
    run_pipeline.run_pipeline()
    assert called == EXPECTED_SEQUENCE
