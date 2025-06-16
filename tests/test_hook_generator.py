import sys
import types
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Mock modules to avoid missing dependencies
sys.modules['dotenv'] = types.ModuleType('dotenv')
sys.modules['dotenv'].load_dotenv = lambda: None
sys.modules['openai'] = types.ModuleType('openai')
sys.modules['openai'].api_key = None

from hook_generator import generate_hook_prompt


def test_generate_hook_prompt_contents():
    prompt = generate_hook_prompt(
        keyword="테스트키워드",
        topic="테스트주제",
        source="출처",
        score=1,
        growth=2,
        mentions=3,
    )

    assert "테스트키워드" in prompt
    assert "출처" in prompt
    assert "1" in prompt
    assert "2" in prompt
    assert "3" in prompt


