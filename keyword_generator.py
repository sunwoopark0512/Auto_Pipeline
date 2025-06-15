from typing import List


def generate_keywords(topic: str) -> List[str]:
    """Return a simple list of keywords for the given topic."""
    base = topic.lower().split()
    return [f"{topic} {i}" for i in ("trend", "guide", "tips", "strategy", "2024")]
