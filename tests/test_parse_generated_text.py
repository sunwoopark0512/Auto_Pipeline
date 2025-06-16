import os
import sys
import types
import importlib


def get_parser():
    """Import notion_hook_uploader.parse_generated_text with external modules mocked."""
    sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda **kwargs: None)
    sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda *a, **k: None)
    os.makedirs('logs', exist_ok=True)
    if 'notion_hook_uploader' in sys.modules:
        del sys.modules['notion_hook_uploader']
    module = importlib.import_module('notion_hook_uploader')
    return module.parse_generated_text


def test_parse_standard_response(tmp_path):
    parse = get_parser()
    text = (
        "후킹 문장1: Hook sentence one\n"
        "후킹 문장2: Hook sentence two\n"
        "블로그 초안:\n"
        "첫 문단입니다.\n"
        "두 번째 문단입니다.\n"
        "세 번째 문단입니다.\n"
        "영상 제목:\n"
        "- Awesome Video 1\n"
        "YouTube 제목:\n"
        "- Great Video 2"
    )
    parsed = parse(text)
    assert parsed["hook_lines"] == ["Hook sentence one", "Hook sentence two"]
    assert parsed["blog_paragraphs"] == ["첫 문단입니다."]
    assert parsed["video_titles"] == ["Awesome Video 1", "Great Video 2"]


def test_parse_alternate_format(tmp_path):
    parse = get_parser()
    text = (
        "후킹문장1) hello world\n"
        "후킹문장2) second line\n"
        "블로그 초안\n"
        "1) paragraph A\n"
        "2) paragraph B\n"
        "3) paragraph C\n"
        "영상 제목:\n"
        "- Title1\n"
        "YouTube 제목:\n"
        "- Title2"
    )
    parsed = parse(text)
    assert parsed["hook_lines"] == ["hello world", "second line"]
    assert parsed["blog_paragraphs"] == ["1) paragraph A"]
    assert parsed["video_titles"] == ["Title1", "Title2"]
