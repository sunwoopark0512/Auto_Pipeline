import os
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

from dotenv import load_dotenv
from notion_client import Client as NotionClient
from supabase import create_client, Client as SupabaseClient

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
INSIGHT_TABLE = os.getenv("INSIGHT_TABLE", "performance_summary")

NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_INSIGHT_DB_ID = os.getenv("NOTION_INSIGHT_DB_ID")
UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "0.5"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

supabase: SupabaseClient | None = None
notion: NotionClient | None = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    logging.warning("Supabase credentials missing. fetch_insights will return []")

if NOTION_TOKEN:
    notion = NotionClient(auth=NOTION_TOKEN)

@dataclass
class InsightRecord:
    id: Any
    summary: str
    created_at: str | None = None


def fetch_insights(client: SupabaseClient | None = None) -> List[dict]:
    """Fetch insight rows from Supabase."""
    client = client or supabase
    if client is None:
        return []
    try:
        response = client.table(INSIGHT_TABLE).select("*").execute()
        data = getattr(response, "data", [])
        logging.info("Fetched %d rows from Supabase", len(data))
        return data
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Supabase fetch error: %s", exc)
        return []


def create_notion_page(record: dict, client: NotionClient | None = None) -> None:
    """Upload a single record to Notion."""
    client = client or notion
    if client is None or NOTION_INSIGHT_DB_ID is None:
        logging.error("Notion credentials missing")
        return
    props = {
        "요약": {"title": [{"text": {"content": str(record.get("summary", ""))}}]},
        "SupabaseID": {"rich_text": [{"text": {"content": str(record.get("id", ""))}}]},
        "등록일": {"date": {"start": datetime.utcnow().isoformat() + "Z"}},
    }
    try:
        client.pages.create(parent={"database_id": NOTION_INSIGHT_DB_ID}, properties=props)
        logging.info("Uploaded record %s to Notion", record.get("id"))
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Failed to upload record %s: %s", record.get("id"), exc)


def upload_insights(records: List[dict], client: NotionClient | None = None) -> None:
    """Upload multiple records to Notion."""
    for rec in records:
        create_notion_page(rec, client)
        if UPLOAD_DELAY:
            try:
                import time
                time.sleep(UPLOAD_DELAY)
            except Exception:  # pragma: no cover - sleep errors not expected
                pass


def run() -> None:
    data = fetch_insights()
    if not data:
        logging.info("No insight data fetched")
        return
    upload_insights(data)


if __name__ == "__main__":
    run()
