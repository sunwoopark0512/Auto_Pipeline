import sys
from types import SimpleNamespace
import importlib
import pytest

# helper to import hook_generator with mocked modules

def import_hook_generator(openai_create):
    sys.modules['dotenv'] = SimpleNamespace(load_dotenv=lambda: None)
    sys.modules['openai'] = SimpleNamespace(ChatCompletion=SimpleNamespace(create=openai_create))
    if 'hook_generator' in sys.modules:
        del sys.modules['hook_generator']
    import hook_generator
    return hook_generator


def test_generate_hook_prompt():
    hg = import_hook_generator(lambda **k: None)
    prompt = hg.generate_hook_prompt('키워드', '키', 'Google', 10, 1.2, 5)
    assert '키워드' in prompt
    assert 'Google' in prompt
    assert '10' in prompt
    assert '1.2' in prompt
    assert '5' in prompt


def test_get_gpt_response_retry(monkeypatch):
    calls = {'n': 0}
    def fake_create(**kwargs):
        calls['n'] += 1
        if calls['n'] < 2:
            raise Exception('fail')
        return SimpleNamespace(choices=[SimpleNamespace(message={'content': 'done'})])

    hg = import_hook_generator(fake_create)
    monkeypatch.setattr(hg.time, 'sleep', lambda x: None)
    result = hg.get_gpt_response('prompt', retries=2)
    assert result == 'done'
    assert calls['n'] == 2
