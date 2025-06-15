import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pipeline import run_all_steps


def test_pipeline_execution():
    try:
        result = run_all_steps()
        assert result is not None
        assert "success" in result
    except Exception as e:
        pytest.fail(f"Pipeline failed with error: {e}")
