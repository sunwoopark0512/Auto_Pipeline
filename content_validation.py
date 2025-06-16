import os
import re

# Load banned terms from env or use defaults
DEFAULT_BANNED_TERMS = [
    "스팸",
    "사기",
    "증오",
    "폭력",
    "성인",
    "도박",
]

def _load_banned_terms():
    env = os.getenv("BANNED_TERMS")
    terms = set(t.lower() for t in DEFAULT_BANNED_TERMS)
    if env:
        for term in env.split(','):
            term = term.strip().lower()
            if term:
                terms.add(term)
    return terms

BANNED_TERMS = _load_banned_terms()

AI_DISCLAIMER_PATTERN = re.compile(r"As an AI|저는 AI", re.IGNORECASE)
LINK_PATTERN = re.compile(r"https?://\S+")


def _check_text(text):
    violations = []
    lower = text.lower()
    for term in BANNED_TERMS:
        if term in lower:
            violations.append(f"금지어 포함: '{term}'")
    if AI_DISCLAIMER_PATTERN.search(text):
        violations.append("AI 모델 언급")
    if LINK_PATTERN.search(text):
        violations.append("링크 포함")
    if len(text) > 2000:
        violations.append("2000자 초과")
    return violations


def validate_item(item):
    """Return list of violations for a generated content item."""
    texts = []
    parsed = item.get("parsed")
    if parsed:
        texts.extend(parsed.get("hook_lines", []))
        texts.extend(parsed.get("blog_paragraphs", []))
        texts.extend(parsed.get("video_titles", []))
    else:
        texts.extend(item.get("hook_lines", []))
        texts.extend(item.get("blog_paragraphs", []))
        texts.extend(item.get("video_titles", []))
    if item.get("generated_text"):
        texts.append(item["generated_text"])

    violations = []
    for t in texts:
        if not isinstance(t, str):
            continue
        violations.extend(_check_text(t))
    return violations


def is_valid(item):
    return not validate_item(item)
