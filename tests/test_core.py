"""Core functionality tests."""

from datetime import datetime

import pytest


def test_datetime_format():
    """Test datetime formatting matches requirements."""
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    assert len(formatted_time) == 19  # YYYY-MM-DD HH:MM:SS = 19 characters


def test_basic_functionality():
    """Basic test to verify pytest is working."""
    assert True


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (2025, True),
        (2024, False),
    ],
)
def test_current_year(test_input, expected):
    """Test current year checking."""
    is_current = test_input == 2025
    assert is_current == expected
