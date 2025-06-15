import os
import sys
import types
import importlib.util
import logging
import pytest

# Stub external dependencies before importing the target module
fake_notion = types.ModuleType("notion_client")
fake_notion.Client = lambda *a, **k: None  # type: ignore[attr-defined]
sys.modules.setdefault("notion_client", fake_notion)

fake_dotenv = types.ModuleType("dotenv")
fake_dotenv.load_dotenv = lambda: None  # type: ignore[attr-defined]
sys.modules.setdefault("dotenv", fake_dotenv)

# Avoid file handler setup during import
logging.FileHandler = lambda *a, **k: logging.NullHandler()  # type: ignore[misc,assignment]

spec = importlib.util.spec_from_file_location(
    "notion_hook_uploader",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "notion_hook_uploader.py"),
)
module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
spec.loader.exec_module(module)  # type: ignore[union-attr]
parse_generated_text = module.parse_generated_text


def test_parse_generated_text_basic():
    text = (
        "후킹 문장1: 첫 번째 후킹\n"
        "후킹 문장2: 두 번째 후킹\n"
        "블로그 초안:\n"
        "첫 단락\n"
        "둘째 단락\n"
        "셋째 단락\n"
        "영상 제목:\n"
        "- 비디오 제목1\n"
        "- 비디오 제목2\n"
    )
    parsed = parse_generated_text(text)
    assert parsed["hook_lines"] == ["첫 번째 후킹", "두 번째 후킹"]
    assert parsed["blog_paragraphs"] == ["첫 단락", "둘째 단락", "셋째 단락"]
    assert parsed["video_titles"] == ["비디오 제목1", "비디오 제목2"]


def test_parse_generated_text_partial_missing():
    text = "후킹 문장1: 훅1\n" "블로그 초안: 파라1\n파라2\n파라3\n"
    parsed = parse_generated_text(text)
    assert parsed["hook_lines"] == ["훅1", ""]
    assert parsed["blog_paragraphs"] == ["파라1", "파라2", "파라3"]
    assert parsed["video_titles"] == ["", ""]
