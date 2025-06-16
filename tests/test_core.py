import os
import sys
import types

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Prepare dummy modules before importing target modules
sys.modules.setdefault('dotenv', types.ModuleType('dotenv')).load_dotenv = lambda: None
sys.modules.setdefault('openai', types.ModuleType('openai')).ChatCompletion = types.SimpleNamespace(create=lambda *a, **k: None)
sys.modules.setdefault('notion_client', types.ModuleType('notion_client')).Client = lambda *a, **k: None

os.makedirs('logs', exist_ok=True)

import hook_generator
import notion_hook_uploader


def test_generate_hook_prompt_basic():
    prompt = hook_generator.generate_hook_prompt(
        keyword="키워드",
        topic="키워드",
        source="twitter",
        score=10,
        growth=1.5,
        mentions=100,
    )
    assert "주제: 키워드" in prompt
    assert "출처: twitter" in prompt
    assert "트렌드 점수: 10" in prompt
    assert "성장률: 1.5" in prompt
    assert "트윗 수: 100" in prompt


def test_parse_generated_text_basic():
    sample_text = (
        "후킹문장1: 첫번째 훅\n"
        "후킹문장2: 두번째 훅\n"
        "블로그 초안: 제목\n"
        "문단1\n"
        "문단2\n"
        "문단3\n"
        "영상 제목:\n"
        "- 제목1\n"
        "- 제목2\n"
    )
    parsed = notion_hook_uploader.parse_generated_text(sample_text)
    assert parsed["hook_lines"] == ["첫번째 훅", "두번째 훅"]
    assert parsed["blog_paragraphs"][0].startswith("제목")
    assert parsed["video_titles"][-1] == "제목2"
