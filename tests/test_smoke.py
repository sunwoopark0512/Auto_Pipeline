import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run_pipeline import PIPELINE_SEQUENCE


def test_pipeline_scripts_exist():
    for script in PIPELINE_SEQUENCE:
        assert os.path.exists(script) or os.path.exists(os.path.join('scripts', script))
