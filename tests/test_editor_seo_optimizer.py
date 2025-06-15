import pytest
from editor_seo_optimizer import optimize_text

def test_optimize_text_output():
    input_text = "this is bad written content with errors."
    result = optimize_text(input_text)
    assert isinstance(result, str)
    assert "bad" not in result.lower()  # improvement assumed
