import datetime
import os
from core.notion_client import NotionClient


def summarize_kpi(start_date: str) -> str:
    """Dummy summary generator."""
    return f"Summary since {start_date}"


def generate_weekly_report():
    """지난 7일간 KPI 요약 → Notion 페이지로 자동 발행."""
    start = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    summary = summarize_kpi(start)
    notion = NotionClient(os.getenv("NOTION_API_SECRET"), os.getenv("NOTION_DATABASE_ID"))
    payload = {
        "parent": {"database_id": os.getenv("NOTION_REPORT_DB")},
        "properties": {
            "Name": {"title": [{"text": {"content": f"Weekly Report ({start})"}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": summary}}]},
            }
        ],
    }
    notion.create_page(payload)
