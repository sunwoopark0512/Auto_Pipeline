"""Tests for content_writer module."""
# pylint: disable=too-few-public-methods
# pylint: disable=wrong-import-position

import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from content_writer import generate_article


class DummyChoice:
    """A dummy choice object for mocking."""

    def __init__(self, content: str):
        self.message = MagicMock(content=content)


class DummyResponse:
    """A dummy response object for mocking."""

    def __init__(self, content: str):
        self.choices = [DummyChoice(content)]


def test_generate_article_returns_text():
    """Test generate_article returns expected text."""
    dummy_response = DummyResponse("Generated text")
    with patch("content_writer.OpenAI") as mock_openai:
        instance = mock_openai.return_value
        instance.chat.completions.create.return_value = dummy_response
        result = generate_article("test keyword", word_count=100, tone="friendly")

    assert result == "Generated text"
    instance.chat.completions.create.assert_called_once()
