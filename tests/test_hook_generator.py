import builtins
import importlib
from unittest import mock

import hook_generator


def test_generate_hook_prompt():
    prompt = hook_generator.generate_hook_prompt(
        keyword="test keyword",
        topic="test",
        source="twitter",
        score=1,
        growth=2,
        mentions=3,
    )
    assert "test keyword" in prompt
    assert "twitter" in prompt
    assert "1" in prompt


class DummyResp:
    def __init__(self, content):
        self.choices = [mock.Mock(message={'content': content})]


def test_get_gpt_response_success(monkeypatch):
    called = {}

    def fake_create(**kwargs):
        called['prompt'] = kwargs['messages'][0]['content']
        return DummyResp("answer")

    monkeypatch.setattr(hook_generator.openai.ChatCompletion, "create", fake_create)
    res = hook_generator.get_gpt_response("hi", retries=2)
    assert res == "answer"
    assert called['prompt'] == "hi"


def test_get_gpt_response_retry(monkeypatch):
    calls = []

    def fake_create(**kwargs):
        calls.append(1)
        if len(calls) < 3:
            raise Exception("fail")
        return DummyResp("ok")

    monkeypatch.setattr(hook_generator.openai.ChatCompletion, "create", fake_create)
    res = hook_generator.get_gpt_response("x", retries=3)
    assert res == "ok"
    assert len(calls) == 3


def test_get_gpt_response_fail(monkeypatch):
    def fake_create(**kwargs):
        raise Exception("nope")

    monkeypatch.setattr(hook_generator.openai.ChatCompletion, "create", fake_create)
    res = hook_generator.get_gpt_response("x", retries=2)
    assert res is None
