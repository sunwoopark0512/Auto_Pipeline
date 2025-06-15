import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import run_pipeline


def test_run_pipeline_sequence_order(monkeypatch):
    calls = []

    def fake_run_script(script):
        calls.append(script)
        return True

    monkeypatch.setattr(run_pipeline, "run_script", fake_run_script)
    run_pipeline.run_pipeline()
    assert calls == run_pipeline.PIPELINE_SEQUENCE


def test_run_script_missing_file(tmp_path, monkeypatch):
    missing = "nonexistent.py"
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    result = run_pipeline.run_script(missing)
    assert result is False
