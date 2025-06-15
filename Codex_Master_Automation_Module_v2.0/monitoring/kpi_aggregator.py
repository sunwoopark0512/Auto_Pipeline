import os
import supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON")

client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_metrics_from_channel(content_id: str, channel: str) -> dict:
    """Dummy fetcher for metrics."""
    return {"content_id": content_id, "channel": channel, "views": 0}


def aggregate_kpi(content_id: str, channel: str):
    """조회수·클릭률 등 메트릭을 수집하여 Supabase 테이블에 upsert."""
    metrics = fetch_metrics_from_channel(content_id, channel)
    client.table("performance_tracker").upsert(metrics).execute()
