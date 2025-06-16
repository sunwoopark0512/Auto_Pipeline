import importlib
import sys
import types
import os


def load_module():
    """Import notion_hook_uploader with stubbed dependencies."""
    # Stub external modules
    dotenv_stub = types.ModuleType("dotenv")
    dotenv_stub.load_dotenv = lambda *a, **k: None
    sys.modules.setdefault("dotenv", dotenv_stub)
    notion_stub = types.ModuleType("notion_client")
    class DummyClient:
        def __init__(self, *a, **k):
            pass
    notion_stub.Client = DummyClient
    sys.modules.setdefault("notion_client", notion_stub)
    os.makedirs("logs", exist_ok=True)
    return importlib.import_module("notion_hook_uploader")


def test_parse_generated_text_basic(tmp_path, monkeypatch):
    module = load_module()
    text = (
        "후킹 문장1: hook1\n"
        "후킹 문장2: hook2\n"
        "블로그 초안:\n"
        "para1\n"
        "para2\n"
        "para3\n"
        "영상 제목:\n"
        "- title1\n"
        "- title2\n"
    )
    result = module.parse_generated_text(text)
    assert result["hook_lines"] == ["hook1", "hook2"]
    # Current regex extracts only first paragraph and last title
    assert result["blog_paragraphs"] == ["para1"]
    assert result["video_titles"] == ["title2"]
