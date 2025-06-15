import os
import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from run_pipeline import run_script


def test_duplicate_import(tmp_path, monkeypatch):
    module_name = "dummy_mod"
    script = tmp_path / f"{module_name}.py"
    script.write_text("print('ok')\n")
    monkeypatch.chdir(tmp_path)
    loaded = set()
    assert run_script(module_name, loaded) is True
    with pytest.raises(ImportError):
        run_script(module_name, loaded)

