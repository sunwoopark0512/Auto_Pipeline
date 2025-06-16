import os
import sys
import types

# Ensure directories for logging exist to avoid errors on import
os.makedirs('logs', exist_ok=True)

# Provide dummy modules so imports in production modules don't fail
sys.modules.setdefault('dotenv', types.ModuleType('dotenv'))
sys.modules['dotenv'].load_dotenv = lambda *args, **kwargs: None

class DummyClient:
    def __init__(self, *args, **kwargs):
        pass

sys.modules.setdefault('notion_client', types.ModuleType('notion_client'))
sys.modules['notion_client'].Client = DummyClient

sys.modules.setdefault('openai', types.ModuleType('openai'))
sys.modules['openai'].ChatCompletion = types.SimpleNamespace(create=lambda **kwargs: None)

from hook_generator import generate_hook_prompt
from notion_hook_uploader import parse_generated_text

def test_generate_hook_prompt_includes_values():
    prompt = generate_hook_prompt("키워드", "주제", "출처", 1.1, 2.2, 3)
    assert "주제: 키워드" in prompt
    assert "출처: 출처" in prompt
    assert "트렌드 점수: 1.1" in prompt
    assert "성장률: 2.2" in prompt
    assert "트윗 수: 3" in prompt
    assert prompt.endswith("전문가처럼.")

def test_parse_generated_text_basic():
    sample = """후킹 문장1: 훅1
후킹 문장2: 훅2
블로그 초안:
문단1
문단2
문단3
영상 제목:
- 타이틀1
- 타이틀2"""
    parsed = parse_generated_text(sample)
    assert parsed["hook_lines"] == ["훅1", "훅2"]
    assert parsed["blog_paragraphs"][0] == "문단1"
    assert parsed["video_titles"][0] == "타이틀2"

def test_parse_generated_text_missing_sections():
    parsed = parse_generated_text("no matching sections")
    assert parsed == {
        "hook_lines": ["", ""],
        "blog_paragraphs": ["", "", ""],
        "video_titles": ["", ""]
    }
