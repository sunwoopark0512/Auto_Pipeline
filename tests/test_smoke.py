import importlib
import os
import sys

sys.path.insert(0, os.getcwd())
os.makedirs('logs', exist_ok=True)
os.environ.setdefault('NOTION_API_TOKEN', 'dummy')
os.environ.setdefault('NOTION_KPI_DB_ID', 'dummy')
os.environ.setdefault('NOTION_HOOK_DB_ID', 'dummy')
os.environ.setdefault('OPENAI_API_KEY', 'dummy')


def test_imports():
    modules = [
        'hook_generator',
        'keyword_auto_pipeline',
        'notion_hook_uploader',
        'retry_dashboard_notifier',
        'scripts.notion_uploader',
        'scripts.retry_failed_uploads',
        'scripts.run_codex_pipeline',
        'scripts.parse_failed_gpt',
        'scripts.notify_retry_result',
    ]
    for m in modules:
        importlib.import_module(m)
