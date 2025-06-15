"""
Supabase → priority-channel upload → Supabase update 플로우.

CLI:
    python hook_uploader.py --table content --limit 5
"""

from __future__ import annotations

import argparse
import importlib
import os
from datetime import datetime, timezone
from typing import List, Dict, Any

from supabase import create_client

from uploader_plugins import (
    YouTubeUploader,
    MediumUploader,
    XUploader,
    TistoryUploader,
    BaseUploader,
)

# ────────── ENV ────────── #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

PRIORITY = ["youtube", "medium", "x", "tistory"]
PLUGIN_MAP: Dict[str, BaseUploader] = {
    "youtube": YouTubeUploader(),
    "medium": MediumUploader(),
    "x": XUploader(),
    "tistory": TistoryUploader(),
}


def _get_supa():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_ready_rows(table: str, limit: int) -> List[Dict[str, Any]]:
    return (
        _get_supa()
        .table(table)
        .select("*")
        .eq("publish_ready", True)
        .is_("published", False)
        .limit(limit)
        .execute()
        .data
        or []
    )


def pick_channel(row) -> str:
    """콘텐츠 row의 preferred_channels JSON 배열 우선 + 그리버럴 PRIORITY."""
    prefs = row.get("preferred_channels") or []
    for ch in prefs + PRIORITY:
        if ch in PLUGIN_MAP:
            return ch
    raise ValueError("No valid channel found")


def update_row(table: str, row_id: Any, channel: str, remote_id: str, public_url: str):
    _get_supa().table(table).update(
        {
            "published": True,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "published_channel": channel,
            "remote_id": remote_id,
            "public_url": public_url,
        }
    ).eq("id", row_id).execute()


def publish_batch(table: str, limit: int):
    rows = fetch_ready_rows(table, limit)
    if not rows:
        print("🎉 Nothing to publish.")
        return

    for row in rows:
        ch = pick_channel(row)
        print(f"🚀 Uploading row {row['id']} to {ch}…")
        uploader = PLUGIN_MAP[ch]
        remote_id, public_url = uploader.upload(row)
        update_row(table, row["id"], ch, remote_id, public_url)
        print(f"✅ Row {row['id']} published → {public_url}")


def _cli():
    ap = argparse.ArgumentParser(description="Bulk upload content to channels")
    ap.add_argument("--table", required=True, help="Supabase table name")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()
    publish_batch(args.table, args.limit)


if __name__ == "__main__":
    _cli()
