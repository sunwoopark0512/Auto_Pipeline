"""Tests for fallback handling and performance measurement utilities."""

import os
import sys
# pylint: disable=wrong-import-position

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fallback_handler import handle_fallback
from performance_optimizer import measure_performance


def test_handle_fallback_returns_none() -> None:
    """``handle_fallback`` should run without raising exceptions."""
    handle_fallback("step", "error")
    assert True


def test_measure_performance_decorator() -> None:
    """Decorator should not alter function return value."""

    @measure_performance
    def sample(x):
        return x * 2

    assert sample(3) == 6
