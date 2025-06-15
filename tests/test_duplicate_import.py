import sys
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run_pipeline


def test_duplicate_import_raises(tmp_path):
    src = "def main(): pass"
    (tmp_path / "dup.py").write_text(src)
    (tmp_path / "dup_alias.py").write_text(src)
    sys.path.insert(0, str(tmp_path))

    run_pipeline._import_and_run("dup")
    with pytest.raises(ImportError):
        run_pipeline._import_and_run("dup_alias")

    sys.path.remove(str(tmp_path))
