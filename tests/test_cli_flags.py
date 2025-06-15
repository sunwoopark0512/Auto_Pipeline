import subprocess


def test_only_flag() -> None:
    res = subprocess.run(
        ["python", "run_pipeline.py", "--dry-run", "--only", "hook_generator.py"],
        text=True,
        capture_output=True,
    )
    assert "hook_generator.py" in res.stdout
    assert "notion_hook_uploader.py" not in res.stdout
