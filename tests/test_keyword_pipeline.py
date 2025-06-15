"""Tests for keyword selection helpers."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from keyword_auto_pipeline import select_top_keywords, Keyword


def test_select_top_keywords_dedup_and_sort():
    """Ensure deduplication and tie-breaking work."""
    rows: list[Keyword] = [
        {"keyword": "a", "cpc": 500.0, "search_volume": 100},
        {"keyword": "b", "cpc": 1000.0, "search_volume": 50},
        {"keyword": "a", "cpc": 700.0, "search_volume": 80},
        {"keyword": "c", "cpc": 700.0, "search_volume": 120},
    ]
    result = select_top_keywords(rows, limit=2)
    assert len(result) == 2
    # keyword b should come first due to highest cpc
    assert result[0]["keyword"] == "b"
    # between a(700) and c(700), c has higher search_volume so should be chosen
    assert result[1]["keyword"] == "c"


def test_select_top_keywords_limit_and_duplicate():
    """Ensure limit and duplicate handling works."""
    rows: list[Keyword] = [
        {"keyword": "x", "cpc": 300.0, "search_volume": 10},
        {"keyword": "x", "cpc": 400.0, "search_volume": 20},
        {"keyword": "y", "cpc": 200.0, "search_volume": 30},
    ]
    result = select_top_keywords(rows, limit=1)
    assert len(result) == 1
    assert result[0]["keyword"] == "x"
    assert result[0]["cpc"] == 400.0
