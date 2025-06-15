import sys
import types

# Dummy modules for dependencies
sys.modules['openai'] = types.SimpleNamespace(
    ChatCompletion=types.SimpleNamespace(create=lambda **kwargs: None)
)
sys.modules['dotenv'] = types.SimpleNamespace(load_dotenv=lambda: None)

# Replace ChatCompletion with controllable class
class DummyCompletion:
    calls = 0
    responses = []

    @classmethod
    def create(cls, **kwargs):
        cls.calls += 1
        resp = cls.responses.pop(0)
        if isinstance(resp, Exception):
            raise resp
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message={'content': resp})])

sys.modules['openai'].ChatCompletion = DummyCompletion

import hook_generator


def test_generate_hook_prompt():
    prompt = hook_generator.generate_hook_prompt('키워드', '키워드', 'Google', 80, 1.5, 100)
    assert '키워드' in prompt
    assert 'Google' in prompt
    assert '80' in prompt
    assert prompt.startswith('주제')


def test_get_gpt_response_retry_success(monkeypatch):
    DummyCompletion.calls = 0
    DummyCompletion.responses = [Exception('fail'), Exception('fail'), 'ok']
    monkeypatch.setattr(hook_generator, 'time', types.SimpleNamespace(sleep=lambda x: None))
    result = hook_generator.get_gpt_response('prompt', retries=3)
    assert result == 'ok'
    assert DummyCompletion.calls == 3


def test_get_gpt_response_all_fail(monkeypatch):
    DummyCompletion.calls = 0
    DummyCompletion.responses = [Exception('fail'), Exception('fail'), Exception('fail')]
    monkeypatch.setattr(hook_generator, 'time', types.SimpleNamespace(sleep=lambda x: None))
    result = hook_generator.get_gpt_response('prompt', retries=3)
    assert result is None
    assert DummyCompletion.calls == 3
