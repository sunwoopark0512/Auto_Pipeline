import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import hook_generator as hg


def test_generate_hook_prompt_basic():
    prompt = hg.generate_hook_prompt(
        keyword="AI marketing",
        topic="AI",
        source="test",
        score=50,
        growth=1.2,
        mentions=100,
    )
    assert "AI marketing" in prompt


def test_get_gpt_response_success(monkeypatch):
    class Resp:
        choices = [type('obj', (), {'message': {'content': 'ok'}})]

    monkeypatch.setattr(hg.openai.ChatCompletion, 'create', lambda **_: Resp())
    assert hg.get_gpt_response('hi') == 'ok'


def test_get_gpt_response_retry(monkeypatch):
    calls = {'n': 0}

    def fake_create(**_):
        calls['n'] += 1
        if calls['n'] < 3:
            raise RuntimeError('fail')
        return type('R', (), {'choices': [type('obj', (), {'message': {'content': 'done'}})]})()

    monkeypatch.setattr(hg.openai.ChatCompletion, 'create', fake_create)
    assert hg.get_gpt_response('hi', retries=3) == 'done'
    assert calls['n'] == 3


def test_generate_hooks_missing_api(monkeypatch, tmp_path):
    monkeypatch.setattr(hg, 'OPENAI_API_KEY', None)
    monkeypatch.setattr(hg, 'KEYWORD_JSON_PATH', str(tmp_path / 'k.json'))
    hg.generate_hooks()  # should exit quietly


def test_generate_hooks_file_error(monkeypatch, tmp_path):
    monkeypatch.setattr(hg, 'OPENAI_API_KEY', 'x')
    monkeypatch.setattr(hg, 'KEYWORD_JSON_PATH', str(tmp_path / 'missing.json'))
    hg.generate_hooks()  # handles file read error gracefully
