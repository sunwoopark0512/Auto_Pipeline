"""Generate keywords for a given topic."""

from typing import List


def generate_keywords(topic: str) -> List[str]:
    """Return a simple list of keywords for the topic."""
    return [f"{topic} example1", f"{topic} example2"]
