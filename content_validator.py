import logging
import re

# List of banned terms or phrases that violate platform policies
BANNED_TERMS = [
    "guaranteed",
    "make money fast",
    "성인",
    "도박",
]


def contains_banned_term(text: str):
    """Check if the text contains any banned term.

    Returns a tuple of (is_valid, offending_term).
    """
    for term in BANNED_TERMS:
        if re.search(term, text, re.IGNORECASE):
            return False, term
    return True, None


def validate_content(parsed: dict) -> bool:
    """Validate parsed hook content.

    The parsed dictionary should contain lists under the keys 'hook_lines',
    'blog_paragraphs' and 'video_titles'. If any banned term is found in the
    text fields this function returns False.
    """
    texts = []
    texts.extend(parsed.get("hook_lines", []))
    texts.extend(parsed.get("blog_paragraphs", []))
    texts.extend(parsed.get("video_titles", []))

    for text in texts:
        valid, term = contains_banned_term(text)
        if not valid:
            logging.error(f"❌ 금지어 발견: '{term}' in '{text}'")
            return False
    return True
