"""
Compute cross-channel performance matrix and suggest next-use priority.

Usage (CLI):
    python osmu_analytics.py --table content --days 7 --limit 10
"""

import os
import argparse
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

import pandas as pd
from supabase import create_client

# ───────── 환경변수 ───────── #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# KPI 필드
KPI_FIELDS = {
    "youtube": "youtube_views",
    "medium": "medium_reads",
    "x": "x_engagement",
    "tistory": "tistory_views",
}

PRIORITY_TABLE = "osmu_priority"  # 결과 저장 테이블


def _get_client():
    if not (SUPABASE_URL and SUPABASE_KEY):
        raise EnvironmentError("Supabase creds missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_recent(table: str, days: int, limit: int) -> pd.DataFrame:
    """최근 days일 내 publish_ready=False 레코드 가져와 DataFrame으로."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    supa = _get_client()
    data = (
        supa.table(table)
        .select("*")
        .gte("published_at", since)
        .order("published_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )
    return pd.DataFrame(data or [])


def compute_priority(df: pd.DataFrame) -> pd.DataFrame:
    """채널별 KPI 비율을 계산하고 우선순위 점수 컬럼 추가."""
    if df.empty:
        return df
    # normalize each KPI to [0,1]
    for ch, field in KPI_FIELDS.items():
        if field in df:
            vals = df[field].astype(float)
            df[f"{ch}_norm"] = (vals - vals.min()) / (vals.max() - vals.min() + 1e-6)
        else:
            df[f"{ch}_norm"] = 0.0
    # 우선순위 점수: 채널별 normalized KPI 가중합
    df["priority_score"] = df[[f"{c}_norm" for c in KPI_FIELDS]].mean(axis=1)
    return df


def publish_priority(df: pd.DataFrame):
    """우선순위 테이블에 결과를 업서트(upsert)."""
    supa = _get_client()
    for _, row in df.iterrows():
        props: Dict[str, Any] = {
            "content_id": row["id"],
            "priority_score": float(row["priority_score"]),
            "computed_at": datetime.now(timezone.utc).isoformat(),
        }
        supa.table(PRIORITY_TABLE).upsert(props, on_conflict="content_id").execute()


def process(table: str, days: int, limit: int):
    df = fetch_recent(table, days, limit)
    df = compute_priority(df)
    if df.empty:
        print("🎉 No recent content to analyze.")
        return
    publish_priority(df)
    print(f"✅ Processed {len(df)} items. Priority table updated.")


def _cli():
    p = argparse.ArgumentParser(description="OSMU Analytics")
    p.add_argument("--table", required=True, help="Supabase source table")
    p.add_argument("--days", type=int, default=7, help="Lookback days")
    p.add_argument("--limit", type=int, default=50, help="Max items")
    args = p.parse_args()
    process(args.table, args.days, args.limit)


if __name__ == "__main__":
    _cli()
