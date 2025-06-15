import pytest
from content_writer import generate_article

def test_generate_article_output():
    result = generate_article("blockchain adoption", 500)
    assert isinstance(result, str)
    assert len(result.split()) >= 400
