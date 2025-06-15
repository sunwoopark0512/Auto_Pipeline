def generate_keywords(topic: str) -> list[str]:
    """Return a list of dummy keywords for the given topic."""
    return [f"{topic} idea {i}" for i in range(1, 3)]
