import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import types
import openai
from hook_generator import generate_hook_prompt, get_gpt_response

class DummyResponse:
    def __init__(self, content):
        self.choices = [types.SimpleNamespace(message={'content': content})]

def test_generate_hook_prompt_includes_values():
    prompt = generate_hook_prompt(
        keyword="ai marketing",
        topic="ai",
        source="Google",
        score=90,
        growth=1.5,
        mentions=123,
    )
    assert "ai marketing" in prompt
    assert "90" in prompt
    assert "1.5" in prompt
    assert "123" in prompt


def test_get_gpt_response_success_after_retries(monkeypatch):
    calls = {
        'count': 0
    }

    def fake_chatcompletion_create(*args, **kwargs):
        calls['count'] += 1
        if calls['count'] < 3:
            raise Exception("temp fail")
        return DummyResponse("hello")

    monkeypatch.setattr(openai.ChatCompletion, 'create', fake_chatcompletion_create)
    result = get_gpt_response("prompt", retries=3)
    assert result == "hello"
    assert calls['count'] == 3


def test_get_gpt_response_all_fail(monkeypatch):
    def fake_fail(*args, **kwargs):
        raise Exception("fail")

    monkeypatch.setattr(openai.ChatCompletion, 'create', fake_fail)
    result = get_gpt_response("prompt", retries=2)
    assert result is None
