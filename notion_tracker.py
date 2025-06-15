#!/usr/bin/env python3
"""
notion_tracker.py
콘텐츠 메타데이터 및 성과 추적
- 콘텐츠 제목, 상태, 발행일, 조회수 등 성과 지표를 Notion DB에 자동 기록
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict

import requests

# 환경변수에서 Notion API 키와 DB ID를 불러옵니다.
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Notion API URL
NOTION_API_URL = "https://api.notion.com/v1/pages"


def create_notion_page(title: str, status: str, platform: str, post_date: str, views: int) -> bool:
    """Create a new page in the configured Notion database."""
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }

    post_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title}}]},
            "Status": {"select": {"name": status}},
            "Platform": {"select": {"name": platform}},
            "Post Date": {"date": {"start": post_date}},
            "Views": {"number": views},
        },
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=post_data, timeout=10)
    if response.status_code == 200:
        print(f"✅ Notion 페이지가 생성되었습니다: {title}")
        return True
    print(f"❌ Notion 페이지 생성 실패: {response.text}")
    return False


def update_notion_page(page_id: str, views: int) -> bool:
    """Update an existing Notion page with new metrics."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }

    update_data = {"properties": {"Views": {"number": views}}}
    response = requests.patch(url, headers=headers, json=update_data, timeout=10)
    if response.status_code == 200:
        print(f"✅ Notion 페이지가 업데이트되었습니다: {page_id}")
        return True
    print(f"❌ Notion 페이지 업데이트 실패: {response.text}")
    return False


def track_performance(content_info: Dict[str, Any]) -> bool:
    """Record content performance to Notion."""
    title = content_info.get("title", "")
    status = content_info.get("status", "")
    platform = content_info.get("platform", "")
    post_date = content_info.get("post_date", str(datetime.now().date()))
    views = int(content_info.get("views", 0))
    return create_notion_page(title, status, platform, post_date, views)


if __name__ == "__main__":
    example = {
        "title": "2025년 여행지 추천: 몰타",
        "status": "Published",
        "platform": "WordPress",
        "post_date": str(datetime.now().date()),
        "views": 1200,
    }
    track_performance(example)
