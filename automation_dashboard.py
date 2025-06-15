#!/usr/bin/env python3
"""
automation_dashboard.py
전체 콘텐츠 자동화 흐름 시각화 및 관리 대시보드
- 콘텐츠 생성, 발행, 성과 추적 등 자동화된 전체 프로세스를 대시보드 형태로 관리
"""

import os
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

# 환경변수에서 Notion API 키와 DB ID를 불러옵니다.
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Notion API URL
NOTION_API_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"


def fetch_notion_data():
    """Notion DB에서 콘텐츠 데이터를 가져옵니다."""
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }
    response = requests.post(NOTION_API_URL, headers=headers)

    if response.status_code == 200:
        print("✅ Notion 데이터 로드 완료.")
        return response.json().get("results", [])
    else:
        print(f"❌ Notion 데이터 로드 실패: {response.text}")
        return []


def generate_dashboard_chart(data: list):
    """자동화된 콘텐츠 발행 및 성과를 바탕으로 시각화된 대시보드 차트 생성"""
    platforms = []
    views = []
    post_dates = []

    for item in data:
        platform = item["properties"]["Platform"]["select"]["name"]
        views_count = item["properties"]["Views"]["number"]
        post_date = item["properties"]["Post Date"]["date"]["start"]
        platforms.append(platform)
        views.append(views_count)
        post_dates.append(post_date)

    # 성과 차트 생성 (조회수 기반)
    plt.figure(figsize=(12, 8))
    plt.barh(platforms, views, color="green")
    plt.xlabel("조회수")
    plt.ylabel("플랫폼")
    plt.title("플랫폼별 콘텐츠 조회수")
    plt.tight_layout()

    # 차트 저장
    chart_filename = (
        f"automation_dashboard_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    )
    plt.savefig(chart_filename)
    plt.close()
    print(f"✅ 대시보드 차트 저장 완료: {chart_filename}")
    return chart_filename


def update_dashboard_with_chart(chart_filename: str):
    """대시보드 차트를 Notion에 업로드하여 시각화"""
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }

    # 이미지 파일을 Notion에 업로드하는 로직 (예시로 가정)
    with open(chart_filename, "rb") as f:
        image_data = f.read()

    # 실제 업로드 기능은 Notion API에서 제공하는 이미지 업로드 API를 이용해야 합니다.
    image_url = "https://example.com/your_uploaded_image_url.png"  # 업로드된 이미지 URL

    post_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": "자동화 콘텐츠 대시보드"}}]},
            "Chart": {"rich_text": [{"text": {"content": image_url}}]},
            "Date": {"date": {"start": str(datetime.now().date())}},
        },
    }

    response = requests.post(url, headers=headers, json=post_data)

    if response.status_code == 200:
        print("✅ 대시보드에 차트 업데이트 완료.")
    else:
        print(f"❌ 대시보드 업데이트 실패: {response.text}")


def main():
    """전체 콘텐츠 자동화 대시보드 생성 및 업데이트"""
    data = fetch_notion_data()
    if not data:
        print("❌ 대시보드 생성 실패: 데이터 없음")
        return

    chart_filename = generate_dashboard_chart(data)
    update_dashboard_with_chart(chart_filename)


if __name__ == "__main__":
    main()
