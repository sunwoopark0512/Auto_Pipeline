"""Tests for run_pipeline module."""

from __future__ import annotations

import subprocess
from pathlib import Path
from shutil import copyfile

from pytest import MonkeyPatch  # pylint: disable=import-error


def test_run_pipeline_normal() -> None:
    """Pipeline should exit with code 0 in dry-run mode."""

    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python", str(repo_root / "run_pipeline.py"), "--dry-run"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0


def test_run_pipeline_duplicate_detection(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """Duplicate module files should trigger ImportError and exit code 1."""

    dup = tmp_path / "dup_step.py"
    dup.write_text("def main(): pass")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "dup_step.py").write_text("def main(): pass")

    repo_root = Path(__file__).resolve().parents[1]
    copyfile(repo_root / "run_pipeline.py", tmp_path / "run_pipeline.py")
    (tmp_path / "scripts").mkdir(exist_ok=True)
    copyfile(repo_root / "scripts" / "logger.py", tmp_path / "scripts" / "logger.py")
    copyfile(
        repo_root / "scripts" / "__init__.py", tmp_path / "scripts" / "__init__.py"
    )
    monkeypatch.chdir(tmp_path)
    result = subprocess.run(
        ["python", "run_pipeline.py", "--only", "dup_step.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "duplicate_module" in result.stderr


def test_run_pipeline_failure_exit_code(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """A failing step should cause the pipeline to exit with code 1."""

    (tmp_path / "fail_step.py").write_text(
        "def main():\n    raise RuntimeError('boom')\n"
    )

    repo_root = Path(__file__).resolve().parents[1]
    copyfile(repo_root / "run_pipeline.py", tmp_path / "run_pipeline.py")
    (tmp_path / "scripts").mkdir(exist_ok=True)
    copyfile(repo_root / "scripts" / "logger.py", tmp_path / "scripts" / "logger.py")
    copyfile(
        repo_root / "scripts" / "__init__.py", tmp_path / "scripts" / "__init__.py"
    )

    monkeypatch.chdir(tmp_path)
    result = subprocess.run(
        ["python", "run_pipeline.py", "--only", "fail_step.py"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "step_failed" in result.stderr


def test_run_pipeline_root_step(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Steps located at the repository root should load and execute."""

    (tmp_path / "simple_step.py").write_text("def main():\n    print('ok')\n")

    repo_root = Path(__file__).resolve().parents[1]
    copyfile(repo_root / "run_pipeline.py", tmp_path / "run_pipeline.py")
    (tmp_path / "scripts").mkdir(exist_ok=True)
    copyfile(repo_root / "scripts" / "logger.py", tmp_path / "scripts" / "logger.py")
    copyfile(
        repo_root / "scripts" / "__init__.py", tmp_path / "scripts" / "__init__.py"
    )

    monkeypatch.chdir(tmp_path)
    result = subprocess.run(
        ["python", "run_pipeline.py", "--only", "simple_step.py"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "step_completed" in result.stderr
