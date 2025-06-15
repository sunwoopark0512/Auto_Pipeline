"""Unit tests for the pipeline orchestrator."""

from pathlib import Path
import sys

# Ensure project root on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pipeline_orchestrator as po  # pylint: disable=wrong-import-position


def test_run_script_success(tmp_path):
    """Ensure run_script returns True for a valid script."""
    script = tmp_path / "hello.py"
    script.write_text('print("hi")')
    assert po.run_script(str(script)) is True


def test_run_script_missing():
    """run_script should gracefully fail when file is absent."""
    assert po.run_script('non_existent.py') is False
