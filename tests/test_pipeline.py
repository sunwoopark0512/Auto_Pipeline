import importlib.util
import pathlib
import os
from run_pipeline import PIPELINE_SEQUENCE


def load_module(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_pipeline_sequence():
    # ensure retry script is included once
    assert PIPELINE_SEQUENCE == [
        "hook_generator.py",
        "notion_hook_uploader.py",
        "retry_failed_uploads.py",
        "retry_dashboard_notifier.py",
    ]


def test_retry_failed_env_default(tmp_path, monkeypatch):
    monkeypatch.delenv("REPARSED_OUTPUT_PATH", raising=False)
    monkeypatch.setenv("NOTION_API_TOKEN", "test")
    monkeypatch.setenv("NOTION_HOOK_DB_ID", "test_db")
    script_path = pathlib.Path("scripts/retry_failed_uploads.py")
    module = load_module(script_path)
    assert module.FAILED_PATH == "logs/failed_keywords_reparsed.json"

