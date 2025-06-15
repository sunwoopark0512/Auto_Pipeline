# -------------------- filename: notion_sync.py ------------------------

import os
import argparse
from datetime import datetime, timezone
from typing import List, Dict, Any

import pandas as pd
from notion_client import Client as Notion
from supabase import create_client

# ────────────── ENV ────────────── #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB = os.getenv("NOTION_DB_ID")

# 매핑 필드 설정
SUPABASE_FIELDS = [
    "id", "title", "published_channel", "public_url",
    "youtube_views", "medium_reads", "x_engagement", "tistory_views",
    "priority_score", "published_at"
]


def _get_supa():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def _get_notion():
    return Notion(auth=NOTION_TOKEN)


def fetch_latest(table: str, limit: int = 50) -> pd.DataFrame:
    """Supabase에서 최신 퍼블리시 데이터 로드"""
    data = (
        _get_supa().table(table)
        .select(",".join(SUPABASE_FIELDS))
        .order("published_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )
    return pd.DataFrame(data or [])


def notion_format(row: Dict[str, Any]) -> Dict:
    """Notion 페이지 속성 변환"""
    props = {
        "Content ID": {"number": row["id"]},
        "Title": {"title": [{"text": {"content": row["title"]}}]},
        "Channel": {"select": {"name": row.get("published_channel", "N/A")}},
        "Public URL": {"url": row.get("public_url")},
        "Priority Score": {"number": row.get("priority_score", 0)},
        "YouTube Views": {"number": row.get("youtube_views", 0)},
        "Medium Reads": {"number": row.get("medium_reads", 0)},
        "X Engagement": {"number": row.get("x_engagement", 0)},
        "Tistory Views": {"number": row.get("tistory_views", 0)},
        "Published At": {"date": {"start": row["published_at"]}},
    }
    return props


def sync_to_notion(df: pd.DataFrame):
    notion = _get_notion()
    for _, row in df.iterrows():
        props = notion_format(row)
        notion.pages.create(
            parent={"database_id": NOTION_DB},
            properties=props
        )


def sync(table: str, limit: int = 50):
    df = fetch_latest(table, limit)
    if df.empty:
        print("🎉 No records found to sync.")
        return
    sync_to_notion(df)
    print(f"✅ Synced {len(df)} records to Notion DB.")


def _cli():
    p = argparse.ArgumentParser(description="Sync Supabase → Notion")
    p.add_argument("--table", required=True)
    p.add_argument("--limit", type=int, default=50)
    args = p.parse_args()
    sync(args.table, args.limit)


if __name__ == "__main__":
    _cli()
