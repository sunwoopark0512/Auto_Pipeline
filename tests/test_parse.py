import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from notion_hook_uploader import parse_generated_text


def test_parse_generated_text_normal():
    text = (
        "후킹 문장1: 첫번째 후킹\n"
        "후킹 문장2: 두번째 후킹\n"
        "블로그 초안: 문단1\n문단2\n문단3\n"
        "영상 제목: 제목1\nYouTube 제목: 제목2"
    )
    result = parse_generated_text(text)
    assert result["hook_lines"] == ["첫번째 후킹", "두번째 후킹"]
    assert result["blog_paragraphs"][0] == "문단1"
    assert result["video_titles"] == ["", ""]


def test_parse_generated_text_missing_sections():
    text = "아무 내용이 없습니다"
    result = parse_generated_text(text)
    assert result["hook_lines"] == ["", ""]
    assert result["blog_paragraphs"] == ["", "", ""]
    assert result["video_titles"] == ["", ""]
