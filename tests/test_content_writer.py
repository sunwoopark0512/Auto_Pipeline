import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from content_writer import generate_article


def test_generate_article_output():
    keyword = "AI Marketing Trends"
    result = generate_article(keyword, word_count=300)
    assert isinstance(result, str)
    assert len(result.split()) >= 250
    assert keyword.lower() in result.lower()
