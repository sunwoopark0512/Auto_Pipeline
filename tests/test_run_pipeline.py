"""Tests for the pipeline runner."""

from run_pipeline import PIPELINE_SEQUENCE, run_script

def test_pipeline_sequence_no_missing_scripts():
    """Ensure missing scripts are not included in the sequence."""
    assert "parse_failed_gpt.py" not in PIPELINE_SEQUENCE
    assert "notify_retry_result.py" not in PIPELINE_SEQUENCE

def test_run_script_missing_file():
    """run_script should return False when the file is absent."""
    result = run_script("nonexistent_script.py")
    assert not result
