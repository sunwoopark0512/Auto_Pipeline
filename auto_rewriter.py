"""
Supabase에서 성과가 저조한 콘텐츠를 자동으로 가져와
GPT-4o로 리라이팅 후 다시 Supabase에 업데이트·플래그하는 모듈.

Usage (CLI):
    python auto_rewriter.py --table content --threshold 0.3
"""

from __future__ import annotations

import os
import argparse
from datetime import datetime, timezone
from typing import Any, Dict, List



# --------------------- 환경 변수 --------------------- #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"
LOW_SCORE_FIELD = "engagement_score"      # KPI 필드명 (0.0 ~ 1.0)
REWRITE_FLAG_FIELD = "needs_rewrite"      # bool


# --------------------- GPT 호출 ---------------------- #
def _ask_gpt(original: str, topic: str) -> str:
    """Return an improved version of `original` suited for the given topic."""
    import openai  # local import to allow tests without openai installed

    rsp = openai.ChatCompletion.create(
        model=MODEL,
        api_key=OPENAI_API_KEY,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert content marketer who quickly rewrites"
                    " under-performing copy for higher engagement."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Rewrite the following text for maximum engagement on"
                    f" social media.\n\nTopic: {topic}\n\n### ORIGINAL ###\n{original}"
                ),
            },
        ],
        temperature=0.7,
    )
    return rsp.choices[0].message.content.strip()


# ------------------ Supabase 핸들러 ------------------ #
def _get_client():
    """Return a lazily imported Supabase client using env vars."""
    if not (SUPABASE_URL and SUPABASE_KEY):
        raise EnvironmentError("Supabase env vars not set")
    from supabase import create_client  # import here to avoid hard dependency in tests

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_low_performers(table: str, threshold: float) -> List[Dict[str, Any]]:
    """가져오기: KPI가 threshold 이하 & 아직 리라이팅 안 된 레코드."""
    supa = _get_client()
    res = (
        supa.table(table)
        .select("*")
        .lte(LOW_SCORE_FIELD, threshold)
        .is_(REWRITE_FLAG_FIELD, False)
        .execute()
    )
    return res.data or []


def update_rewritten_row(table: str, row_id: Any, new_content: str):
    """Supabase row 업데이트 + rewrite 플래그."""
    supa = _get_client()
    supa.table(table).update(
        {
            "content": new_content,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            REWRITE_FLAG_FIELD: True,
        }
    ).eq("id", row_id).execute()


# ----------------------- 메인 ------------------------ #
def rewrite_batch(table: str, threshold: float, topic_field: str = "topic"):
    """Fetch → GPT rewrite → update 루프."""
    targets = fetch_low_performers(table, threshold)
    if not targets:
        print("🎉 No low performers found.")
        return
    print(f"🔧 Rewriting {len(targets)} item(s)...")

    for item in targets:
        new_content = _ask_gpt(item["content"], item.get(topic_field, "general"))
        update_rewritten_row(table, item["id"], new_content)
        print(f"✅ Row {item['id']} rewritten.")


def _cli():
    parser = argparse.ArgumentParser(description="Auto rewrite poor-performing content")
    parser.add_argument("--table", required=True, help="Supabase table name")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        help="KPI threshold (<= triggers rewrite)",
    )
    args = parser.parse_args()
    rewrite_batch(args.table, args.threshold)


if __name__ == "__main__":
    _cli()
