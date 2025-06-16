import os
import re
import logging

BANNED_KEYWORDS_PATH = os.getenv("BANNED_KEYWORDS_PATH", "config/banned_keywords.txt")
MAX_TEXT_LENGTH = 2000


def load_banned_keywords():
    if os.path.exists(BANNED_KEYWORDS_PATH):
        with open(BANNED_KEYWORDS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []


BANNED_KEYWORDS = load_banned_keywords()


def contains_banned_keyword(text, banned_keywords=None):
    keywords = banned_keywords if banned_keywords is not None else BANNED_KEYWORDS
    lowered = text.lower()
    for kw in keywords:
        if kw.lower() in lowered:
            return kw
    return None


def check_formatting(text):
    if len(text) > MAX_TEXT_LENGTH:
        return False, "text too long"
    if re.search(r"\s{2,}", text):
        return False, "multiple spaces detected"
    return True, ""


def validate_generated_item(item, banned_keywords=None):
    fields = []
    for key in ("hook_lines", "blog_paragraphs", "video_titles"):
        if key in item and isinstance(item[key], list):
            fields.extend(item[key])
    if not fields and "generated_text" in item:
        fields.append(item["generated_text"])

    combined = " ".join(fields)
    kw = contains_banned_keyword(combined, banned_keywords)
    if kw:
        return False, f"banned keyword '{kw}'"

    for field in fields:
        ok, reason = check_formatting(field)
        if not ok:
            return False, reason

    return True, ""
