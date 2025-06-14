"""Smoke test for the pipeline loader."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_pipeline_dry_run_smoke() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python", str(repo_root / "run_pipeline.py"), "--dry-run"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
