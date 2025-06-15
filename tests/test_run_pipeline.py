import os
from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from run_pipeline import run_script


def test_run_script_missing():
    assert not run_script('no_such_script.py')


def test_run_script_success(tmp_path):
    script_name = 'temp_test_script.py'
    root_dir = Path(__file__).resolve().parents[1]
    temp_script = root_dir / script_name
    temp_script.write_text('print("ok")')
    try:
        assert run_script(script_name)
    finally:
        temp_script.unlink()

