import re

CONTENT_GUIDELINES = {
    "notion": {
        "banned_words": ["banned1", "banned2"],
        "max_length": 2000,
    },
    "blog": {
        "banned_words": ["spam", "clickbait"],
        "max_length": 5000,
        "no_urls": True,
    },
}


def validate_text(text: str, platform: str = "notion"):
    """Check text against platform guidelines.

    Returns a tuple (is_valid, reason). is_valid is True if the text passes
    all checks. Otherwise reason contains a short description of the rule that
    was violated.
    """
    guidelines = CONTENT_GUIDELINES.get(platform, {})
    if not text:
        return True, None

    lowered = text.lower()
    for word in guidelines.get("banned_words", []):
        if word.lower() in lowered:
            return False, f"banned word '{word}'"

    if guidelines.get("no_urls") and re.search(r"https?://", text):
        return False, "contains url"

    max_len = guidelines.get("max_length")
    if max_len and len(text) > max_len:
        return False, f"exceeds max length {max_len}"

    return True, None


def ensure_valid(text: str, platform: str = "notion"):
    valid, reason = validate_text(text, platform)
    if not valid:
        raise ValueError(f"{platform} guideline violation: {reason}")

