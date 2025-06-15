import logging
import os
import sys
from types import SimpleNamespace

import run_pipeline


def test_run_script_missing_file(caplog, tmp_path):
    caplog.set_level(logging.ERROR)
    original_dir = run_pipeline.SCRIPTS_DIR
    run_pipeline.SCRIPTS_DIR = str(tmp_path)
    try:
        result = run_pipeline.run_script("does_not_exist.py")
        assert not result
        assert any("파일이 존재하지 않습니다" in r.message for r in caplog.records)
    finally:
        run_pipeline.SCRIPTS_DIR = original_dir


def test_run_script_success(tmp_path):
    script = tmp_path / "dummy.py"
    script.write_text("print('hello')")
    original_dir = run_pipeline.SCRIPTS_DIR
    run_pipeline.SCRIPTS_DIR = str(tmp_path)
    try:
        assert run_pipeline.run_script("dummy.py")
    finally:
        run_pipeline.SCRIPTS_DIR = original_dir


def test_run_pipeline_with_missing_script(monkeypatch, caplog, tmp_path):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr(run_pipeline, "PIPELINE_SEQUENCE", ["missing.py"])
    monkeypatch.setattr(run_pipeline, "SCRIPTS_DIR", str(tmp_path))
    run_pipeline.run_pipeline()
    messages = [r.message for r in caplog.records]
    assert any("파일이 존재하지 않습니다" in msg for msg in messages)
    assert any("일부 단계에서 실패 발생" in msg for msg in messages)
