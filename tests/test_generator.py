"""Tests for docstring generator."""

from typing import List, Optional

import pytest

from docgen.generator import DocstringGenerator, DocstringTemplate


def test_docstring_template():
    """Test docstring template generation."""
    template = DocstringTemplate(
        summary="Test function",
        description="This is a test function",
        args=[("param1", "str", "First parameter")],
        returns=("bool", "Success status"),
        raises=[("ValueError", "If parameter is invalid")],
    )

    docstring = template.generate()
    assert "Test function" in docstring
    assert "This is a test function" in docstring
    assert "param1 (str): First parameter" in docstring
    assert "bool: Success status" in docstring
    assert "ValueError: If parameter is invalid" in docstring


def sample_function(param1: str, param2: Optional[int] = None) -> List[str]:
    """Sample function for testing."""
    return [param1]


def test_analyze_function():
    """Test function analysis."""
    generator = DocstringGenerator()
    template = generator.analyze_function(sample_function)

    assert isinstance(template, DocstringTemplate)
    assert "sample_function" in template.summary
    assert len(template.args) == 2
    assert template.args[0][0] == "param1"
    assert template.args[0][1] == "str"
    assert template.returns[0] == "List"


def test_apply_docstring():
    """Test docstring application."""
    generator = DocstringGenerator()
    template = DocstringTemplate(
        summary="Updated docstring", description="New description"
    )

    def test_func():
        pass

    generator.apply_docstring(test_func, template)
    assert test_func.__doc__ == template.generate()


def test_invalid_input():
    """Test error handling for invalid inputs."""
    generator = DocstringGenerator()

    with pytest.raises(ValueError):
        generator.analyze_function("not a function")

    with pytest.raises(ValueError):
        generator.analyze_class("not a class")
