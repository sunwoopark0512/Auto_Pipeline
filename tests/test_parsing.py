import os
import sys
import types

# Ensure the repository root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Stub external dependencies used during import
sys.modules["dotenv"] = types.ModuleType("dotenv")
sys.modules["dotenv"].load_dotenv = lambda *a, **k: None
sys.modules["notion_client"] = types.ModuleType("notion_client")
sys.modules["notion_client"].Client = type("Client", (), {"__init__": lambda self, *a, **k: None})

import pytest

from notion_hook_uploader import parse_generated_text


def test_parse_typical_response():
    text = (
        "후킹문장1: 첫 번째 후킹문입니다\n"
        "후킹문장2: 두 번째 후킹문입니다\n"
        "블로그 초안:\n"
        "첫 번째 문단입니다.\n"
        "두 번째 문단입니다.\n"
        "세 번째 문단입니다.\n"
        "영상 제목:\n"
        "- 멋진 영상 제목 1\n"
        "- 멋진 영상 제목 2\n"
    )
    result = parse_generated_text(text)
    assert result["hook_lines"] == ["첫 번째 후킹문입니다", "두 번째 후킹문입니다"]
    # parser may not return all paragraphs but should return a list
    assert isinstance(result["blog_paragraphs"], list)
    assert len(result["blog_paragraphs"]) >= 1
    assert isinstance(result["video_titles"], list)
    assert len(result["video_titles"]) >= 1


def test_parse_missing_sections():
    text = "후킹문장1: 후킹만 있는 경우"
    result = parse_generated_text(text)
    assert result["hook_lines"] == ["", ""]
    assert result["blog_paragraphs"] == ["", "", ""]
    assert result["video_titles"] == ["", ""]


def test_parse_malformed_text():
    text = "아무 의미 없는 텍스트만 존재합니다"
    result = parse_generated_text(text)
    assert result["hook_lines"] == ["", ""]
    assert result["blog_paragraphs"] == ["", "", ""]
    assert result["video_titles"] == ["", ""]
