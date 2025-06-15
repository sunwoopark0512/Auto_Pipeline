import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_pipeline

def test_duplicate_import_raises(tmp_path, monkeypatch):
    code = "def main(): pass"
    file_path = tmp_path / "dup.py"
    file_path.write_text(code)
    sys.path.insert(0, str(tmp_path))

    run_pipeline._import_and_run("dup")

    alias_path = tmp_path / "dup_alias.py"
    alias_path.write_text(code)
    with pytest.raises(ImportError):
        run_pipeline._import_and_run("dup_alias")

    sys.path.remove(str(tmp_path))
