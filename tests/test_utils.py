import os
import sys

# Ensure repository root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import types
import importlib
import logging

# Stub external dependencies before importing modules
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)
sys.modules['openai'] = types.SimpleNamespace()
sys.modules['notion_client'] = types.SimpleNamespace(Client=lambda **kw: None)
logging.FileHandler = lambda *args, **kwargs: logging.NullHandler()

import hook_generator
importlib.reload(hook_generator)
import notion_hook_uploader
importlib.reload(notion_hook_uploader)


def test_generate_hook_prompt():
    text = hook_generator.generate_hook_prompt(
        keyword="키워드",
        topic="토픽",
        source="GoogleTrends",
        score=80,
        growth=1.5,
        mentions=100,
    )
    assert "주제: 키워드" in text
    assert "출처: GoogleTrends" in text
    assert "트렌드 점수: 80, 성장률: 1.5, 트윗 수: 100" in text
    assert text.endswith("친근하면서도 전문가처럼.")


def test_parse_generated_text():
    sample = (
        "후킹 문장1: 첫 번째 후킹\n"
        "후킹 문장2: 두 번째 후킹\n"
        "블로그 초안: 첫번째 문단\n"
        "두번째 문단\n"
        "세번째 문단\n"
        "영상 제목:\n"
        "- 제목1\n"
        "영상 제목:\n"
        "- 제목2\n"
    )
    result = notion_hook_uploader.parse_generated_text(sample)
    assert result["hook_lines"] == ["첫 번째 후킹", "두 번째 후킹"]
    assert result["blog_paragraphs"] == ["첫번째 문단"]
    assert result["video_titles"] == ["제목1", "제목2"]
