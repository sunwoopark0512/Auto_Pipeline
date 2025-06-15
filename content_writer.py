from typing import List


def generate_article(topic: str, length: int) -> str:
    """Generate a very basic article for testing purposes."""
    words: List[str] = []
    while len(words) < length:
        words.extend([topic] * 10)
    return " ".join(words[:length])
