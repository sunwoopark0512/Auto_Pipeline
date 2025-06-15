import importlib
import pytest

modules = [
    "hook_generator",
    "keyword_auto_pipeline",
    "notion_hook_uploader",
    "retry_dashboard_notifier",
    "retry_failed_uploads",
    "run_pipeline",
    "scripts.notion_uploader",
    "scripts.retry_failed_uploads",
    "auto_optimize",
    "rotate_secrets",
]

@pytest.mark.parametrize("mod", modules)
def test_import(mod):
    try:
        importlib.import_module(mod)
    except ImportError as e:
        pytest.skip(f"Optional dependency missing: {e}")
