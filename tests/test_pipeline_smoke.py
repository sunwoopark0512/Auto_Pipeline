import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from run_pipeline import PIPELINE_SEQUENCE


def test_pipeline_sequence_defined():
    assert isinstance(PIPELINE_SEQUENCE, list)
    assert len(PIPELINE_SEQUENCE) > 0
