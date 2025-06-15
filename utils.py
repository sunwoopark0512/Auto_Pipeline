"""Utility functions for the Auto_Pipeline project."""

from typing import Any


def truncate_text(text: str, max_length: int = 2000) -> str:
    """Truncate text to fit within Notion's rich_text length limit."""
    return text if len(text) <= max_length else text[:max_length]
