#!/usr/bin/env python3
"""Notion dashboard module for visualizing content performance."""

from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import requests

# Environment variables
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"


def fetch_notion_data() -> list[Any]:
    """Fetch content data from a Notion database."""
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }
    response = requests.post(NOTION_API_URL, headers=headers)
    if response.status_code == 200:
        print("✅ Notion 데이터 로드 완료.")
        return response.json().get("results", [])
    print(f"❌ Notion 데이터 로드 실패: {response.text}")
    return []


def generate_performance_chart(data: list[dict[str, Any]]) -> str:
    """Generate a bar chart based on content views."""
    titles: list[str] = []
    views: list[int] = []
    for item in data:
        title = item["properties"]["Title"]["title"][0]["text"]["content"]
        views_count = item["properties"]["Views"]["number"]
        titles.append(title)
        views.append(views_count)

    plt.figure(figsize=(10, 6))
    plt.barh(titles, views, color="skyblue")
    plt.xlabel("조회수")
    plt.title("콘텐츠 조회수 성과")
    plt.tight_layout()

    chart_filename = f"performance_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    plt.savefig(chart_filename)
    plt.close()
    print(f"✅ 차트 저장 완료: {chart_filename}")
    return chart_filename


def update_notion_dashboard(chart_filename: str) -> None:
    """Update the Notion dashboard with the generated chart."""
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }

    with open(chart_filename, "rb") as file:
        _ = file.read()  # Placeholder for actual upload logic
    image_url = "https://example.com/your_uploaded_image_url.png"

    post_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": "콘텐츠 성과 대시보드"}}]
            },
            "Chart": {
                "rich_text": [{"text": {"content": image_url}}]
            },
            "Date": {"date": {"start": str(datetime.now().date())}},
        },
    }

    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 200:
        print("✅ 대시보드에 차트 업데이트 완료.")
    else:
        print(f"❌ 대시보드 업데이트 실패: {response.text}")


def main() -> None:
    """Create and update the Notion content performance dashboard."""
    data = fetch_notion_data()
    if not data:
        print("❌ 대시보드 생성 실패: 데이터 없음")
        return
    chart_filename = generate_performance_chart(data)
    update_notion_dashboard(chart_filename)


if __name__ == "__main__":
    main()
