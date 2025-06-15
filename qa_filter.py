
def content_safety_check(text: str) -> bool:
    """Simple safety check that flags text containing the word 'bad'."""
    return "bad" not in text.lower()
