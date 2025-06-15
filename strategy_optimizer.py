# -------------------- filename: strategy_optimizer.py ------------------------

import os
import argparse
from datetime import datetime, timedelta, timezone
from typing import Dict, Any

import pandas as pd
import openai
from supabase import create_client

# ────────────── ENV ────────────── #
SUPABASE_URL  = os.getenv("SUPABASE_URL")
SUPABASE_KEY  = os.getenv("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"
OPTIMIZER_TABLE = "strategy_optimizer"

# KPI 필드 (단축)
KPI_FIELDS = [
    "youtube_views", "medium_reads", "x_engagement", "tistory_views",
    "priority_score", "published_channel", "published_at"
]


def _get_supa():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_recent(table: str, days: int = 30) -> pd.DataFrame:
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    supa = _get_supa()
    data = (
        supa.table(table)
        .select(",".join(KPI_FIELDS))
        .gte("published_at", since)
        .execute()
        .data
    )
    return pd.DataFrame(data or [])


def compute_summary(df: pd.DataFrame) -> str:
    """간략한 집계 결과 텍스트 생성"""
    lines = []
    if df.empty:
        return "No recent data available."
    for field in ["youtube_views", "medium_reads", "x_engagement", "tistory_views"]:
        vals = df[field].astype(float)
        lines.append(f"{field}: avg={vals.mean():.1f}, max={vals.max()}, min={vals.min()}")
    return "\n".join(lines)


def gpt_recommend(summary: str) -> Dict[str, Any]:
    """GPT에게 최적화 파라미터 추천 요청"""
    prompt = (
        "You are the AI strategy optimizer for a fully automated multi-channel content system.\n"
        "Based on recent performance data, suggest new parameter values:\n\n"
        "- title_variants (1-5)\n"
        "- thumb_variants (1-5)\n"
        "- rewrite_threshold (0.0-1.0)\n"
        "- upload_limit (1-10)\n"
        "- rewriter_priority (low, medium, high)\n\n"
        f"Recent data summary:\n{summary}\n"
        "Respond ONLY in valid JSON like: { ... }"
    )

    rsp = openai.ChatCompletion.create(
        model=MODEL,
        api_key=OPENAI_API_KEY,
        messages=[{"role":"user", "content":prompt}],
        temperature=0,
    )
    content = rsp.choices[0].message.content
    import json
    return json.loads(content)


def upsert_recommendation(params: Dict[str, Any]):
    supa = _get_supa()
    record = {
        **params,
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }
    supa.table(OPTIMIZER_TABLE).insert(record).execute()


def process(table: str, days: int):
    df = fetch_recent(table, days)
    summary = compute_summary(df)
    recs = gpt_recommend(summary)
    upsert_recommendation(recs)
    print("✅ Strategy optimization recommendation updated:", recs)


def _cli():
    p = argparse.ArgumentParser(description="Strategy Optimizer")
    p.add_argument("--table", required=True)
    p.add_argument("--days", type=int, default=30)
    args = p.parse_args()
    process(args.table, args.days)


if __name__ == "__main__":
    _cli()
