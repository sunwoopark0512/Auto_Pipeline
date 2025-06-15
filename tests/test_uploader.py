import types
import sys

sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda *a, **k: None)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)

from notion_hook_uploader import parse_generated_text


def test_parse_generated_text_basic():
    text = (
        "후킹 문장1: hello\n"
        "후킹 문장2: world\n"
        "블로그 초안:\n"
        "para1\n"
        "para2\n"
        "para3\n"
        "영상 제목: title1\n"
        "YouTube 제목: title2\n"
    )
    result = parse_generated_text(text)
    assert result["hook_lines"][0] == "hello"
    assert result["hook_lines"][1] == "world"
    assert "blog_paragraphs" in result
    assert "video_titles" in result
