"""Content conversion utilities for various platforms."""

from datetime import datetime

# 기본 플랫폼 템플릿
TEMPLATES = {
    "youtube": "제목: {title}\n\n스크립트:\n안녕하세요, 오늘은 {summary}...\n(영상 요소: {elements})",
    "instagram": "{summary}\n\n#해시태그: {hashtags}\n(이미지 설명: {image_desc})",
    "tiktok": "{hook}\n{summary}\n\n{call_to_action}",
    "facebook": "{summary}\n\n자세히 보기: {link}",
    "linkedin": "제목: {title}\n{summary}\n\n전문 읽기: {link}",
}

def convert_content(original_text: str, platform: str) -> str:
    """Convert original content to a specific platform format."""
    title = original_text.split('\n')[0]
    summary = original_text[:100] + "..."

    if platform == "youtube":
        elements = "시각자료 큐, BGM 큐 등"
        return TEMPLATES[platform].format(title=title, summary=summary, elements=elements)
    elif platform == "instagram":
        hashtags = "#자동화 #콘텐츠 #OSMU"
        image_desc = "포스트와 관련된 시각 자료 설명"
        return TEMPLATES[platform].format(summary=summary, hashtags=hashtags, image_desc=image_desc)
    elif platform == "tiktok":
        hook = "📣 " + title + " 📣\n"
        call_to_action = "👉 더 알고 싶다면 댓글을 확인하세요!"
        return TEMPLATES[platform].format(hook=hook, summary=summary, call_to_action=call_to_action)
    elif platform == "facebook":
        link = "https://example.com/full-post"
        return TEMPLATES[platform].format(summary=summary, link=link)
    elif platform == "linkedin":
        link = "https://example.com/full-post"
        return TEMPLATES[platform].format(title=title, summary=summary, link=link)
    else:
        return original_text
