from unittest import mock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import keyword_content_generator as kc


def test_generate_keywords_parses_lines():
    fake_response = mock.Mock()
    fake_response.choices = [mock.Mock(message=mock.Mock(content="kw1\nkw2\n"))]
    with mock.patch('keyword_content_generator.OpenAI') as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = fake_response
        result = kc.generate_keywords("test")
    assert result == ["kw1", "kw2"]
