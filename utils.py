"""Utility functions for Auto_Pipeline scripts."""

def truncate_text(text: str, max_length: int = 2000) -> str:
    """Return text truncated to the max_length suitable for Notion rich text."""
    return text if len(text) <= max_length else text[:max_length]

