"""
Aggregate performance metrics from Supabase → GPT-4o summary →
publish to Notion database as a new Page.

CLI:
    python auto_insight.py --table content --days 7 --notion-db MY_DB_ID
"""

from __future__ import annotations

import os
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import openai
import pandas as pd
from notion_client import Client as Notion
from supabase import create_client


# ------------------ ENVIRONMENT ------------------ #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

MODEL = "gpt-4o"
METRIC_FIELD = "engagement_score"


# ------------------ DATA LAYER ------------------- #
def _get_supa():
    if not (SUPABASE_URL and SUPABASE_KEY):
        raise EnvironmentError("Supabase env vars missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_range(table: str, days: int) -> pd.DataFrame:
    """Fetch last `days` of content rows into DataFrame."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    data = (
        _get_supa()
        .table(table)
        .select("*")
        .gte("created_at", since)
        .execute()
        .data
    )
    return pd.DataFrame(data or [])


# ------------------ ANALYTICS -------------------- #
def summarize_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute basic stats for METRIC_FIELD."""
    if df.empty:
        return {"count": 0}
    metric = df[METRIC_FIELD].astype(float)
    return {
        "count": len(metric),
        "avg": float(metric.mean()),
        "median": float(metric.median()),
        "p90": float(metric.quantile(0.9)),
        "best_id": int(df.loc[metric.idxmax()]["id"]),
        "worst_id": int(df.loc[metric.idxmin()]["id"]),
    }


def gpt_insight(stats: Dict[str, Any], horizon: int) -> str:
    """Return text insight from GPT."""
    prompt = (
        "You are a senior growth analyst. Based on the stats and time horizon,"
        " write a concise (~150 words) executive insight with one actionable tip."
        f"\n\nHORIZON_DAYS={horizon}\nSTATS={stats}"
    )
    rsp = openai.ChatCompletion.create(
        model=MODEL,
        api_key=OPENAI_API_KEY,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return rsp.choices[0].message.content.strip()


# ------------------ NOTION ----------------------- #
def notion_publish(db_id: str, title: str, text: str, stats: Dict[str, Any]):
    notion = Notion(auth=NOTION_TOKEN)
    props = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Count": {"number": stats.get("count", 0)},
        "Avg": {"number": stats.get("avg")},
        "Median": {"number": stats.get("median")},
        "p90": {"number": stats.get("p90")},
    }
    notion.pages.create(
        parent={"database_id": db_id},
        properties=props,
        children=[{"object": "block", "type": "paragraph", "paragraph": {"text": [{"type": "text", "text": {"content": text}}]}}],
    )


# ------------------ MAIN ------------------------- #
def generate_insight(table: str, days: int, notion_db: str):
    df = fetch_range(table, days)
    stats = summarize_metrics(df)
    insight = gpt_insight(stats, days)
    title = f"Insight {datetime.now().strftime('%Y-%m-%d')}"
    notion_publish(notion_db, title, insight, stats)
    print(f"\u2705 Notion page created: {title}")


def _cli():
    parser = argparse.ArgumentParser(description="Generate weekly insight")
    parser.add_argument("--table", required=True)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--notion-db", required=True)
    args = parser.parse_args()
    generate_insight(args.table, args.days, args.notion_db)


if __name__ == "__main__":
    _cli()
