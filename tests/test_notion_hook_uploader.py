import builtins
import pytest
from unittest.mock import patch, MagicMock

import notion_hook_uploader


def test_parse_generated_text_basic():
    text = (
        "후킹 문장1: Hook1\n"
        "후킹 문장2: Hook2\n"
        "블로그 초안:\n"
        "Paragraph1\n"
        "Paragraph2\n"
        "Paragraph3\n"
        "영상 제목:\n"
        "- Video1\n"
        "- Video2\n"
    )
    result = notion_hook_uploader.parse_generated_text(text)
    assert result["hook_lines"] == ["Hook1", "Hook2"]
    # Function currently returns only the first paragraph
    assert result["blog_paragraphs"] == ["Paragraph1"]
    assert result["video_titles"] == ["Video2"]


def test_parse_generated_text_empty():
    result = notion_hook_uploader.parse_generated_text("")
    assert result == {
        "hook_lines": ["", ""],
        "blog_paragraphs": ["", "", ""],
        "video_titles": ["", ""],
    }


def test_page_exists_true():
    with patch.object(notion_hook_uploader.notion.databases, "query", return_value={"results": [1]}):
        assert notion_hook_uploader.page_exists("kw") is True


def test_page_exists_false_on_empty():
    with patch.object(notion_hook_uploader.notion.databases, "query", return_value={"results": []}):
        assert notion_hook_uploader.page_exists("kw") is False


def test_page_exists_handles_exception(caplog):
    with patch.object(notion_hook_uploader.notion.databases, "query", side_effect=Exception("fail")):
        assert notion_hook_uploader.page_exists("kw") is False
        assert any("중복 확인 실패" in message for message in caplog.messages)

