#!/usr/bin/env python3
"""
notion_kpi_tracker.py
- Notion DB의 콘텐츠 메타데이터를 수집해 KPI 계산
- 목표치 대비 달성률을 산출하고 KPI 대시보드 페이지를 자동 업데이트
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict

# Notion API 설정
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_KPI_DB_ID = os.getenv("NOTION_KPI_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# ──────────────────────────────────────────────────────────────────────────────
# 1. 데이터 수집
# ──────────────────────────────────────────────────────────────────────────────
def fetch_content_records(days: int = 7) -> List[Dict]:
    """최근 N일간 게시물 레코드 조회"""
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    payload = {
        "filter": {"property": "Post Date", "date": {"after": since}}
    }
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    res = requests.post(url, headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json().get("results", [])

# ──────────────────────────────────────────────────────────────────────────────
# 2. KPI 계산
# ──────────────────────────────────────────────────────────────────────────────
def calculate_kpis(records: List[Dict], kpi_targets: Dict[str, float]) -> Dict[str, Dict]:
    """기본 KPI(조회수·좋아요·CTR)와 목표 대비 달성률 산출"""
    views = [r["properties"]["Views"]["number"] for r in records]
    likes = [r["properties"].get("Likes", {"number": 0})["number"] for r in records]
    impressions = [
        r["properties"].get("Impressions", {"number": 0})["number"]
        for r in records
    ]

    total_views = sum(views)
    total_likes = sum(likes)
    total_imps = sum(impressions)
    ctr = (total_views / total_imps) * 100 if total_imps else 0
    like_rate = (total_likes / total_views) * 100 if total_views else 0

    kpis = {
        "Total Views": total_views,
        "Total Impressions": total_imps,
        "CTR (%)": round(ctr, 2),
        "Like‑Rate (%)": round(like_rate, 2),
    }

    progress = {
        name: f"{(value / kpi_targets.get(name, 1)) * 100:.1f}%"
        for name, value in kpis.items()
        if isinstance(value, (int, float))
    }

    return {"kpis": kpis, "progress": progress}

# ──────────────────────────────────────────────────────────────────────────────
# 3. Notion KPI 대시보드 갱신
# ──────────────────────────────────────────────────────────────────────────────
def upsert_kpi_page(report: Dict[str, Dict], period_label: str) -> None:
    """KPI 결과를 KPI DB에 '업서트'"""
    query_url = f"https://api.notion.com/v1/databases/{NOTION_KPI_DB_ID}/query"
    payload = {"filter": {"property": "Period", "rich_text": {"equals": period_label}}}
    res = requests.post(query_url, headers=HEADERS, json=payload)
    res.raise_for_status()
    existing = res.json().get("results", [])

    def props() -> Dict:
        return {
            "Title": {"title": [{"text": {"content": f"KPI 보고서 {period_label}"}}]},
            "Period": {"rich_text": [{"text": {"content": period_label}}]},
            **{
                key: {"number": val if isinstance(val, (int, float)) else None}
                for key, val in report["kpis"].items()
            },
            **{
                f"{k} Progress": {"rich_text": [{"text": {"content": v}}]}
                for k, v in report["progress"].items()
            },
        }

    if existing:
        page_id = existing[0]["id"]
        url = f"https://api.notion.com/v1/pages/{page_id}"
        requests.patch(url, headers=HEADERS, json={"properties": props()})
        print(f"🔄 KPI 페이지 업데이트 완료 → {period_label}")
    else:
        url = "https://api.notion.com/v1/pages"
        requests.post(
            url,
            headers=HEADERS,
            json={"parent": {"database_id": NOTION_KPI_DB_ID}, "properties": props()},
        )
        print(f"✅ KPI 페이지 생성 완료 → {period_label}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. 실행 엔트리포인트
# ──────────────────────────────────────────────────────────────────────────────
def main(days: int = 7) -> None:
    """최근 N일치 KPI 산출 후 대시보드 기록"""
    records = fetch_content_records(days)
    if not records:
        print("📭 최근 게시물 없음 – KPI 계산 스킵")
        return

    KPI_TARGETS = {
        "Total Views": 10000,
        "Total Impressions": 50000,
        "CTR (%)": 8,
        "Like‑Rate (%)": 3,
    }

    report = calculate_kpis(records, KPI_TARGETS)
    period = f"{days}‑Day ({datetime.utcnow().date()})"
    upsert_kpi_page(report, period)

if __name__ == "__main__":
    main(days=7)
