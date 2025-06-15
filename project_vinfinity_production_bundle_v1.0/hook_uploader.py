"""Simulate uploading content to WordPress."""

from typing import Tuple, Dict


def upload_to_wordpress(title: str, content: str, slug: str, token: str) -> Tuple[int, Dict[str, str]]:
    """Return a dummy status code and response."""
    return 201, {"url": f"https://example.com/{slug}"}
