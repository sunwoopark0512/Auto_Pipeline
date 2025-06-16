import importlib
import types
import sys
import os

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Stub missing openai module to avoid import errors
sys.modules['openai'] = types.ModuleType('openai')

import hook_generator as hg

def test_generate_hook_prompt():
    prompt = hg.generate_hook_prompt(
        keyword="테스트 키워드",
        topic="테스트",
        source="Twitter",
        score=80,
        growth=1.5,
        mentions=100
    )
    assert "테스트 키워드" in prompt
    assert "Twitter" in prompt
    assert "80" in prompt
    assert "1.5" in prompt
    assert "100" in prompt
