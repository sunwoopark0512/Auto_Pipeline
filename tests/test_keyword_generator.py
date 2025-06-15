import pytest
from keyword_generator import generate_keywords

def test_generate_keywords_output():
    result = generate_keywords("blockchain technology")
    assert isinstance(result, list)
    assert len(result) >= 5
