import re

# Simple platform guidelines with example banned terms and formatting rules
GUIDELINES = {
    "notion": {
        "banned_terms": ["spam", "subscribe", "buy now"],
        # Example forbidden pattern: raw URLs are not allowed in Notion text
        "forbidden_patterns": [r"https?://[^\s]+"],
    },
    "youtube": {
        "banned_terms": ["subscribe", "like and share"],
        "forbidden_patterns": [],
    },
    "blog": {
        "banned_terms": ["click here", "buy now"],
        "forbidden_patterns": [],
    },
}


def detect_violation(text: str, platform: str = "notion"):
    """Return a string describing the violation if the text violates rules."""
    rules = GUIDELINES.get(platform, {})
    lower_text = text.lower()
    for term in rules.get("banned_terms", []):
        if term.lower() in lower_text:
            return f"banned term '{term}'"
    for pattern in rules.get("forbidden_patterns", []):
        if re.search(pattern, text):
            return f"forbidden pattern '{pattern}'"
    return None


def check_parsed_content(parsed: dict, platform: str = "notion"):
    """Check parsed content sections for violations."""
    for section in ("hook_lines", "blog_paragraphs", "video_titles"):
        for text in parsed.get(section, []):
            if not text:
                continue
            violation = detect_violation(text, platform=platform)
            if violation:
                return violation, text
    return None, None
