import re

# ---------------------- 기본 정책 ----------------------
# 금지어와 금지 패턴은 실제 운영 가이드라인을 반영해 업데이트한다.
BANNED_WORDS = [
    "욕설",
    "비속어",
    "불법",
    "성인",
    "음란",
]

BANNED_PATTERNS = [
    r"(?:http|https)://[^\s]+",  # 외부 링크 금지 예시
]


def validate_text(text: str):
    """텍스트가 정책을 준수하는지 검사한다."""
    if not text:
        return True, None
    lower = text.lower()
    for word in BANNED_WORDS:
        if word.lower() in lower:
            return False, f"금지어 포함: {word}"
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, f"금지 표현 발견: {pattern}"
    return True, None


def validate_hook_item(item: dict):
    """후킹 생성 결과 전체를 점검한다."""
    fields = []
    if "keyword" in item:
        fields.append(item["keyword"])
    if "generated_text" in item:
        fields.append(item["generated_text"])
    for key in ["hook_lines", "blog_paragraphs", "video_titles"]:
        value = item.get(key)
        if isinstance(value, list):
            fields.extend(value)
    for text in fields:
        ok, reason = validate_text(text)
        if not ok:
            return False, reason
    return True, None
