import re

BANNED_KEYWORDS = ["hate", "violence", "extremism"]


def check_ethics(text: str) -> bool:
    """단순 키워드 + 정규식 기반 1차 필터."""
    for kw in BANNED_KEYWORDS:
        if re.search(rf"\b{kw}\b", text, flags=re.I):
            return False
    return True
