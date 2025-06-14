"""Smoke test for pipeline loading."""

import subprocess


def test_run_pipeline_dry_run() -> None:
    """Ensure the pipeline runner exits successfully in dry-run mode."""

    result = subprocess.run(
        ["python", "run_pipeline.py", "--dry-run"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
