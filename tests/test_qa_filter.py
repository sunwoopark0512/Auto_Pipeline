import pytest
from qa_filter import content_safety_check

def test_content_safety_check_output():
    result = content_safety_check("This is safe content.")
    assert isinstance(result, bool)
