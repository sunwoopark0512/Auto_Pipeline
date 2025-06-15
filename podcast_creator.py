"""
Fetch content rows flagged for podcast → generate MP3 via TTS →
upload to Supabase Storage → append to local RSS feed → mark as done.

Usage (CLI):
    python podcast_creator.py --table content --limit 5
"""

import os
import argparse
from datetime import datetime, timezone
from typing import List, Dict

from gtts import gTTS
from supabase import create_client


# ───────────────── 환경변수 ───────────────── #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
RSS_FILE = os.getenv("PODCAST_RSS_FILE", "podcast_feed.xml")
BUCKET = "podcasts"


def _get_client():
    if not (SUPABASE_URL and SUPABASE_KEY):
        raise EnvironmentError("Supabase credentials missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_pending(table: str, limit: int) -> List[Dict]:
    """generate_podcast=True & podcast_generated=False rows."""
    supa = _get_client()
    res = (
        supa.table(table)
        .select("*")
        .eq("generate_podcast", True)
        .is_("podcast_generated", False)
        .limit(limit)
        .execute()
    )
    return res.data or []


def generate_audio(text: str, lang: str = "en") -> str:
    """TTS로 MP3 생성, 로컬 파일명 반환."""
    fname = f"podcast_{int(datetime.now().timestamp())}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(fname)
    return fname


def upload_audio(file_path: str) -> str:
    """Supabase Storage에 업로드 후 public URL 반환."""
    supa = _get_client()
    with open(file_path, "rb") as f:
        supa.storage.from_(BUCKET).upload(file_path, f)
    url = supa.storage.from_(BUCKET).get_public_url(file_path)["publicURL"]
    return url


def append_rss(item_id: int, title: str, url: str):
    """간단한 RSS <item> 블록을 로컬 RSS 파일에 추가."""
    entry = f"""
  <item>
    <guid isPermaLink="false">{item_id}</guid>
    <title>{title}</title>
    <link>{url}</link>
    <pubDate>{datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>
  </item>
"""
    with open(RSS_FILE, "a", encoding="utf-8") as rss:
        rss.write(entry)


def mark_done(table: str, row_id: int, file_name: str, url: str):
    """DB에 podcast_generated, podcast_url, podcast_id 업데이트."""
    supa = _get_client()
    supa.table(table).update(
        {
            "podcast_generated": True,
            "podcast_url": url,
            "podcast_id": file_name,
            "podcast_generated_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", row_id).execute()


def process_batch(table: str, limit: int):
    rows = fetch_pending(table, limit)
    if not rows:
        print("🎉 No pending podcasts.")
        return

    for row in rows:
        print(f"🔊 Generating podcast for row {row['id']}…")
        file_name = generate_audio(row["content"])
        url = upload_audio(file_name)
        append_rss(row["id"], row["title"], url)
        mark_done(table, row["id"], file_name, url)
        print(f"✅ Podcast created → {url}")


def _cli():
    p = argparse.ArgumentParser(description="Auto podcast generator")
    p.add_argument("--table", required=True, help="Supabase table name")
    p.add_argument("--limit", type=int, default=5)
    args = p.parse_args()
    process_batch(args.table, args.limit)


if __name__ == "__main__":
    _cli()
