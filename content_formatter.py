# -------------------- filename: content_formatter.py ---------------------
"""
자동으로 콘텐츠를 채널별 요구 사항에 맞춰 포맷팅하는 모듈.
각 채널에 필요한 길이, 해시태그, 썸네일 텍스트 분리 등을 포함합니다.

CLI:
    python content_formatter.py --table content --limit 5
"""

from __future__ import annotations

import argparse
from typing import Dict, Any, cast

from googletrans import Translator  # type: ignore

# 각 채널의 템플릿 예시
CHANNEL_TEMPLATES = {
    "youtube": {
        "title_max": 100,
        "content_max": 4900,  # YouTube에서는 설명이 5000자 이하
        "hashtags": "#YouTube #ContentCreation",
    },
    "medium": {
        "title_max": 60,
        "content_max": 2000,
        "hashtags": "#Medium #Blogging",
    },
    "x": {
        "title_max": 280,
        "content_max": 280,
        "hashtags": "#X #ShortText",
    },
    "tistory": {
        "title_max": 70,
        "content_max": 1000,
        "hashtags": "#Tistory #Blogging",
    },
}


def format_for_channel(row: Dict[str, Any], channel: str) -> Dict[str, Any]:
    """주어진 행(row)을 채널 포맷에 맞춰 변환한다."""
    template = CHANNEL_TEMPLATES.get(channel)
    if not template:
        raise ValueError(f"Channel {channel} not supported.")

    title_max = cast(int, template["title_max"])
    content_max = cast(int, template["content_max"])
    title = row.get("title", "")[: title_max]
    content = row.get("content", "")[: content_max]
    content += f"\n\n{template['hashtags']}"
    thumbnail_text = row.get("content", "")[:50]
    return {
        "formatted_title": title,
        "formatted_content": content,
        "thumbnail_text": thumbnail_text,
    }


def translate_content(row: Dict[str, Any], target_lang: str = "en") -> Dict[str, Any]:
    """주어진 행(row)을 target_lang 언어로 번역한다."""
    translator = Translator()
    translated_title = translator.translate(row.get("title", ""), dest=target_lang).text
    translated_content = translator.translate(row.get("content", ""), dest=target_lang).text
    return {
        "translated_title": translated_title,
        "translated_content": translated_content,
    }


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Auto format content for channels")
    parser.add_argument("--table", required=True, help="Supabase table name")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    rows = [
        {
            "id": 1,
            "title": "Exciting YouTube Video!",
            "content": "This is an amazing video on YouTube about technology and coding.",
        }
    ]

    for row in rows[: args.limit]:
        for channel in CHANNEL_TEMPLATES.keys():
            formatted = format_for_channel(row, channel)
            print(f"Formatted content for {channel}: {formatted}")


if __name__ == "__main__":
    _cli()
