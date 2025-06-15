"""
Fetch content rows flagged for graphic creation \u2192 generate infographic via DALL\xb7E \u2192
download & upload to Supabase Storage \u2192 update DB with graphic_url.

Usage (CLI):
    python graphic_generator.py --table content --limit 5
"""

import os
import argparse
import requests
from io import BytesIO
from datetime import datetime, timezone
from typing import List, Dict

import openai
from PIL import Image
from supabase import create_client

# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \ud658\uacbd\ubcc0\uc218 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \nOPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL    = os.getenv("SUPABASE_URL")
SUPABASE_KEY    = os.getenv("SUPABASE_ANON_KEY")
GRAPHIC_BUCKET  = "graphics"

# \ud544\ub4dc\uba85
FIELD_ID             = "id"
FIELD_CONTENT        = "content"
FIELD_TITLE          = "title"
FIELD_GEN_GRAPHIC    = "generate_graphic"
FIELD_GRAPHIC_DONE   = "graphic_generated"
FIELD_GRAPHIC_URL    = "graphic_url"


def _get_client():
    if not (SUPABASE_URL and SUPABASE_KEY):
        raise EnvironmentError("Supabase credentials missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_pending(table: str, limit: int) -> List[Dict]:
    """generate_graphic=True & graphic_generated=False rows."""
    supa = _get_client()
    res = (
        supa.table(table)
        .select("*")
        .eq(FIELD_GEN_GRAPHIC, True)
        .is_(FIELD_GRAPHIC_DONE, False)
        .limit(limit)
        .execute()
    )
    return res.data or []


def generate_image(prompt: str, size: str = "512x512") -> str:
    """Call DALL\xb7E to generate an image, return URL."""
    openai.api_key = OPENAI_API_KEY
    resp = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size
    )
    return resp["data"][0]["url"]


def download_image(url: str) -> BytesIO:
    """Download image bytes."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return BytesIO(r.content)


def upload_to_storage(file_bytes: BytesIO, filename: str) -> str:
    """Upload image to Supabase Storage, return public URL."""
    supa = _get_client()
    # reset cursor
    file_bytes.seek(0)
    supa.storage.from_(GRAPHIC_BUCKET).upload(filename, file_bytes)
    return supa.storage.from_(GRAPHIC_BUCKET).get_public_url(filename)["publicURL"]


def update_row(table: str, row_id: int, url: str):
    """Mark row with graphic_url and graphic_generated flag."""
    supa = _get_client()
    supa.table(table).update({
        FIELD_GRAPHIC_URL: url,
        FIELD_GRAPHIC_DONE: True,
        "graphic_generated_at": datetime.now(timezone.utc).isoformat(),
    }).eq(FIELD_ID, row_id).execute()


def process_batch(table: str, limit: int):
    rows = fetch_pending(table, limit)
    if not rows:
        print("\ud83c\udf89 No graphics to generate.")
        return

    for row in rows:
        vid = row[FIELD_ID]
        title = row.get(FIELD_TITLE, "") or ""
        snippet = row[FIELD_CONTENT][:100]  # \uc694\uc57d\uc6a9 \ud14d\uc2a4\ud2b8
        prompt = f"Create an infographic summarizing the following:\nTitle: {title}\nContent: {snippet}..."
        print(f"\ud83c\udfa8 Generating graphic for row {vid}\u2026")
        img_url = generate_image(prompt)
        img_bytes = download_image(img_url)
        fname = f"graphic_{vid}_{int(datetime.now().timestamp())}.png"
        public_url = upload_to_storage(img_bytes, fname)
        update_row(table, vid, public_url)
        print(f"\u2705 Row {vid} graphic uploaded \u2192 {public_url}")


def _cli():
    p = argparse.ArgumentParser(description="Auto graphic (infographic) generator")
    p.add_argument("--table", required=True, help="Supabase table name")
    p.add_argument("--limit", type=int, default=5, help="Max rows to process")
    args = p.parse_args()
    process_batch(args.table, args.limit)


if __name__ == "__main__":
    _cli()
