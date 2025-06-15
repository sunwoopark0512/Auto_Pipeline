"""
Generate A/B title & thumbnail-text variants via GPT and mark rows for test.

Usage (CLI):
    python ab_variant_manager.py --table content --limit 5 \
        --title-variants 3 --thumb-variants 2
"""

import os
import argparse
from typing import List, Dict, Any

import openai
from supabase import create_client

# ──────────────── 환경 변수 & 기본값 ──────────────── #
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# 필드명
FIELD_CONTENT = "content"
FIELD_TITLE = "title"
FIELD_ID = "id"
FIELD_TITLE_VARIANTS = "title_variants"          # JSON[]
FIELD_THUMB_VARIANTS = "thumb_text_variants"      # JSON[]
FIELD_AB_READY = "ab_test_ready"                  # bool


def _get_client():
    if not (SUPABASE_URL and SUPABASE_KEY):
        raise EnvironmentError("Supabase env vars missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_rows(table: str, limit: int) -> List[Dict[str, Any]]:
    """generate variants가 False인 최근 rows를 가져옵니다."""
    supa = _get_client()
    res = (
        supa.table(table)
        .select("*")
        .is_(FIELD_AB_READY, False)
        .limit(limit)
        .execute()
    )
    return res.data or []

def _ask_variants(prompt: str) -> List[str]:
    rsp = openai.ChatCompletion.create(  # type: ignore[attr-defined]
        model=MODEL,
        api_key=OPENAI_API_KEY,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    text = rsp.choices[0].message.content.strip()
    # GPT 응답을 줄 단위로 분할
    variants = [line.strip(" -") for line in text.splitlines() if line.strip()]
    return variants


def generate_variants_for_row(row: Dict[str, Any], title_n: int, thumb_n: int) -> Dict[str, Any]:
    title = row[FIELD_TITLE]
    content = row[FIELD_CONTENT]

    # 제목 variants prompt
    title_prompt = (
        f"Generate {title_n} concise, click-worthy title variants "
        f"for this article:\n\n\"{title}\""
    )
    titles = _ask_variants(title_prompt)[:title_n]

    # 썬데일 테스트 variants prompt
    thumb_prompt = (
        f"Generate {thumb_n} short thumbnail text snippets "
        f"(<=50 chars) summarizing:\n\n\"{content[:200]}...\""
    )
    thumbs = _ask_variants(thumb_prompt)[:thumb_n]

    return {
        FIELD_TITLE_VARIANTS: titles,
        FIELD_THUMB_VARIANTS: thumbs,
    }


def update_row(table: str, row_id: int, updates: Dict[str, Any]):
    supa = _get_client()
    supa.table(table).update({
        **updates,
        FIELD_AB_READY: True
    }).eq(FIELD_ID, row_id).execute()


def process_batch(table: str, limit: int, title_n: int, thumb_n: int):
    rows = fetch_rows(table, limit)
    if not rows:
        print("🎉 No rows needing variants.")
        return

    for row in rows:
        vid = row[FIELD_ID]
        print(f"🔄 Generating A/B variants for row {vid}...")
        vars = generate_variants_for_row(row, title_n, thumb_n)
        update_row(table, vid, vars)
        print(f"✅ Row {vid} updated with {title_n} titles and {thumb_n} thumbs.")


def _cli():
    p = argparse.ArgumentParser(description="A/B variant generator")
    p.add_argument("--table", required=True, help="Supabase table name")
    p.add_argument("--limit", type=int, default=5, help="Max rows to process")
    p.add_argument("--title-variants", type=int, default=2, help="Number of title variants")
    p.add_argument("--thumb-variants", type=int, default=2, help="Number of thumbnail text variants")
    args = p.parse_args()
    process_batch(args.table, args.limit, args.title_variants, args.thumb_variants)


if __name__ == "__main__":
    _cli()
