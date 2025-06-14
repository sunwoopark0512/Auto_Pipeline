import os
import subprocess
from pathlib import Path
from textwrap import dedent
from types import ModuleType
import importlib.util
import sys
import pytest


def _stub(name: str, tmp: Path, fail: bool = False) -> None:
    if name == "notifier":
        func = "def main(failures=None):\n    print(failures)\n"
    else:
        func = "def main():\n    " + ("raise RuntimeError('fail')\n" if fail else "print('ok')\n")
    (tmp / f"{name}.py").write_text(func)


@pytest.mark.parametrize("folder", [".", "scripts"])
def test_dynamic_import(folder, tmp_path: Path):
    module_name = "sample"
    target_dir = tmp_path / folder
    target_dir.mkdir(exist_ok=True)
    _stub(module_name, target_dir)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import run_pipeline as rp
    rp.BASE_DIR = tmp_path
    mod = rp._dynamic_import(module_name)
    assert hasattr(mod, "main")


def test_execution_order(tmp_path: Path, monkeypatch):
    order = ["a", "b", "c", "notifier"]
    for name in order[:-1]:
        _stub(name, tmp_path)
    _stub("notifier", tmp_path)

    monkeypatch.chdir(tmp_path)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    runner = tmp_path / "runner.py"
    runner.write_text(
        dedent(
            f"""
            from pathlib import Path
            from run_pipeline import main
            import run_pipeline as rp
            rp.PIPELINE_ORDER = {order}
            rp.BASE_DIR = Path('.')
            """
        )
    )
    spec = importlib.util.spec_from_file_location("runner", runner)
    assert spec and spec.loader
    mod: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    mod.main()  # type: ignore[attr-defined]


def test_notifier_called_on_failure(tmp_path: Path):
    order = ["fail_step", "notifier"]
    _stub("fail_step", tmp_path, fail=True)
    (tmp_path / "notifier.py").write_text("def main(failures):\n    print(failures)\n")
    run_py = tmp_path / "run.py"
    run_py.write_text(
        dedent(
            f"""
            import sys
            sys.path.insert(0, '{Path(__file__).resolve().parents[1]}')
            import run_pipeline as rp
            rp.PIPELINE_ORDER = {order}
            rp.main()
            """
        )
    )
    proc = subprocess.run([sys.executable, str(run_py)], cwd=tmp_path, capture_output=True, text=True)
    assert "fail_step" in proc.stdout


def test_duplicate_detection(tmp_path: Path):
    base = tmp_path / "task.py"
    base.write_text("def main():\n    pass\n")
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "alias.py").symlink_to(base)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import run_pipeline as rp
    rp.BASE_DIR = tmp_path
    rp.PIPELINE_ORDER = ["task", "alias", "notifier"]
    _stub("notifier", tmp_path)
    with pytest.raises(SystemExit):
        rp.main([])


def test_dry_run(tmp_path: Path, capsys):
    order = ["step", "notifier"]
    _stub("step", tmp_path)
    _stub("notifier", tmp_path)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import run_pipeline as rp
    rp.BASE_DIR = tmp_path
    rp.PIPELINE_ORDER = order
    rp.main(["--dry-run"])
    captured = capsys.readouterr()
    assert "step_start step" in captured.out
    assert os.environ.get("DRY_RUN") == "1"


def test_exit_code_on_failure(tmp_path: Path):
    order = ["boom", "notifier"]
    _stub("boom", tmp_path, fail=True)
    _stub("notifier", tmp_path)
    run_py = tmp_path / "run.py"
    run_py.write_text(
        dedent(
            f"""
            import sys, os
            sys.path.insert(0, '{Path(__file__).resolve().parents[1]}')
            import run_pipeline as rp
            rp.BASE_DIR = Path('.')
            rp.PIPELINE_ORDER = {order}
            rp.main([])
            """
        )
    )
    proc = subprocess.run([sys.executable, str(run_py)], cwd=tmp_path)
    assert proc.returncode == 1

