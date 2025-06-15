import types
import sys
import time

import pytest

import hook_generator


def test_generate_hook_prompt():
    prompt = hook_generator.generate_hook_prompt(
        keyword="keyword1",
        topic="topic1",
        source="Twitter",
        score=10,
        growth=1.5,
        mentions=100,
    )
    assert "주제: keyword1" in prompt
    assert "출처: Twitter" in prompt
    assert "트렌드 점수: 10" in prompt
    assert "성장률: 1.5" in prompt
    assert "트윗 수: 100" in prompt


def test_get_gpt_response(monkeypatch):
    class MockChoice:
        def __init__(self, content):
            self.message = {"content": content}

    class MockResponse:
        def __init__(self, content):
            self.choices = [MockChoice(content)]

    calls = []

    def mock_create(**kwargs):
        calls.append(kwargs)
        return MockResponse("hello")

    monkeypatch.setattr(hook_generator.openai.ChatCompletion, "create", mock_create)
    result = hook_generator.get_gpt_response("hi")
    assert result == "hello"
    assert len(calls) == 1


def test_get_gpt_response_retries(monkeypatch):
    class MockChoice:
        def __init__(self, content):
            self.message = {"content": content}

    class MockResponse:
        def __init__(self, content):
            self.choices = [MockChoice(content)]

    attempts = {"count": 0}

    def mock_create(**kwargs):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise Exception("fail")
        return MockResponse("ok")

    monkeypatch.setattr(hook_generator.openai.ChatCompletion, "create", mock_create)
    monkeypatch.setattr(time, "sleep", lambda x: None)
    result = hook_generator.get_gpt_response("hi", retries=2)
    assert result == "ok"
    assert attempts["count"] == 2
