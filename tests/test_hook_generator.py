import importlib
import sys
import types
import os


def load_module():
    dotenv_stub = types.ModuleType("dotenv")
    dotenv_stub.load_dotenv = lambda *a, **k: None
    sys.modules.setdefault("dotenv", dotenv_stub)
    openai_stub = types.ModuleType("openai")
    openai_stub.api_key = ""
    sys.modules.setdefault("openai", openai_stub)
    return importlib.import_module("hook_generator")


def test_generate_hook_prompt_basic():
    module = load_module()
    prompt = module.generate_hook_prompt(
        keyword="테스트 키워드",
        topic="테스트",
        source="test-source",
        score=80,
        growth=1.5,
        mentions=100,
    )
    assert "테스트 키워드" in prompt
    assert "test-source" in prompt
    assert "80" in prompt
    assert "1.5" in prompt
    assert "100" in prompt
