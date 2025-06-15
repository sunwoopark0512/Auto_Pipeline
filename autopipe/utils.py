"""Common utility functions for autopipe package."""

from typing import Any

def truncate_text(text: str, max_len: int = 2000) -> str:
    """Return the text truncated to the given max length."""
    return text if len(text) <= max_len else text[:max_len]

