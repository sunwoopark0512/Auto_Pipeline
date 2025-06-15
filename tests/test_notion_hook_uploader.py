import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import os; os.makedirs("logs", exist_ok=True)
from notion_hook_uploader import parse_generated_text

SAMPLE_TEXT = """
후킹 문장1: 첫 문장
후킹 문장2: 둘째 문장
블로그 초안:
첫째 문단
둘째 문단
셋째 문단
영상 제목:
- 비디오 제목1
- 비디오 제목2
"""


def test_parse_generated_text_basic():
    parsed = parse_generated_text(SAMPLE_TEXT)
    assert parsed['hook_lines'] == ['첫 문장', '둘째 문장']
    assert parsed["blog_paragraphs"][0] == "첫째 문단"
    assert parsed["video_titles"] == ["비디오 제목2"]
