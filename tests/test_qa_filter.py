"""Tests for the qa_filter module."""

from types import SimpleNamespace
import qa_filter


class DummyClient:  # pylint: disable=too-few-public-methods
    """Simple stand-in for the OpenAI client used in tests."""

    def __init__(self, response: str) -> None:
        message = SimpleNamespace(content=response)
        choice = SimpleNamespace(message=message)
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda model, messages: SimpleNamespace(choices=[choice])
            )
        )


def test_content_safety_check_safe(monkeypatch):
    """The function should return True when the API responds with 'NO'."""
    monkeypatch.setattr(qa_filter, "OpenAI", lambda: DummyClient("NO"))
    assert qa_filter.content_safety_check("hello") is True


def test_content_safety_check_unsafe(monkeypatch):
    """The function should return False when the API responds with 'YES'."""
    monkeypatch.setattr(qa_filter, "OpenAI", lambda: DummyClient("YES"))
    assert qa_filter.content_safety_check("bad stuff") is False
