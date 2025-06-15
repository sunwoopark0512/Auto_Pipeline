import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from parse_failed_gpt import parse_generated_text

def test_parse_generated_text_basic():
    text = """후킹 문장1: 첫 문장\n후킹 문장2: 두번째\n블로그 초안:\n첫번째\n두번째\n세번째\n영상 제목:\n제목1\n제목2"""
    result = parse_generated_text(text)
    assert result["hook_lines"] == ["첫 문장", "두번째"]
    assert result["blog_paragraphs"] == ["첫번째", "두번째", "세번째"]
    assert result["video_titles"] == ["제목1", "제목2"]
