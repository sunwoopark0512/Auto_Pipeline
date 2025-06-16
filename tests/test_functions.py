import sys
import types
import logging

# Provide stub modules for external dependencies
sys.modules['dotenv'] = types.ModuleType('dotenv')
sys.modules['dotenv'].load_dotenv = lambda: None
sys.modules['openai'] = types.ModuleType('openai')
sys.modules['notion_client'] = types.ModuleType('notion_client')
sys.modules['notion_client'].Client = lambda *a, **k: None

class DummyFileHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def emit(self, record):
        pass
logging.FileHandler = DummyFileHandler

import hook_generator
import notion_hook_uploader


def test_generate_hook_prompt():
    result = hook_generator.generate_hook_prompt(
        keyword="AI Marketing",
        topic="AI",
        source="Twitter",
        score=80,
        growth=1.5,
        mentions=1000,
    )
    expected = (
        "주제: AI Marketing\n"
        "    출처: Twitter\n"
        "    트렌드 점수: 80, 성장률: 1.5, 트윗 수: 1000\n"
        "    이 정보를 기반으로:\n"
        "    - 숏폼 영상의 후킹 문장 2개\n"
        "    - 블로그 포스트의 3문단 초안\n"
        "    - YouTube 영상 제목 예시 2개\n"
        "    를 마케팅적으로 끌리는 문장으로 생성해줘. 말투는 친근하면서도 전문가처럼."
    )
    assert result == expected


def test_parse_generated_text():
    sample = (
        "후킹 문장1: 첫 후킹 문장입니다.\n"
        "후킹 문장2: 두 번째 후킹 문장입니다.\n"
        "블로그 초안:\n"
        "첫 번째 문단입니다.\n"
        "두 번째 문단입니다.\n"
        "세 번째 문단입니다.\n"
        "영상 제목: 멋진 영상1\n"
        "- 멋진 영상2"
    )
    parsed = notion_hook_uploader.parse_generated_text(sample)
    assert parsed["hook_lines"] == ["첫 후킹 문장입니다.", "두 번째 후킹 문장입니다."]
    assert parsed["blog_paragraphs"] == ["첫 번째 문단입니다."]
    assert parsed["video_titles"] == ["멋진 영상2"]
