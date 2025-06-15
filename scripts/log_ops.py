import os
import logging
import argparse
import datetime
from typing import Dict, Any

import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore


load_dotenv()

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_OPS_DB_ID")
NOTION_VERSION = "2022-06-28"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


MAX_TEXT_LENGTH = 2000


def _clip(text: str, max_length: int = MAX_TEXT_LENGTH) -> str:
    return text if len(text) <= max_length else text[:max_length]


def build_payload(**data: str) -> Dict[str, Any]:
    now = datetime.datetime.now().isoformat()
    return {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Log Type": {"select": {"name": data["log_type"]}},
            "Date": {"date": {"start": now}},
            "Operator": {"title": [{"text": {"content": data["operator"]}}]},
            "Module": {"rich_text": [{"text": {"content": _clip(data["module"])}}]},
            "Environment": {"select": {"name": data["environment"]}},
            "Task Summary": {"rich_text": [{"text": {"content": _clip(data["task_summary"])}}]},
            "Action Details": {"rich_text": [{"text": {"content": _clip(data["action_details"])}}]},
            "Verification": {"rich_text": [{"text": {"content": _clip(data.get("verification", ""))}}]},
            "Error Summary": {"rich_text": [{"text": {"content": _clip(data.get("error_summary", ""))}}]},
            "Root Cause": {"rich_text": [{"text": {"content": _clip(data.get("root_cause", ""))}}]},
            "Resolution": {"rich_text": [{"text": {"content": _clip(data.get("resolution", ""))}}]},
            "Patch Details": {"rich_text": [{"text": {"content": _clip(data.get("patch_details", ""))}}]},
            "Release Version": {"rich_text": [{"text": {"content": _clip(data.get("release_version", ""))}}]},
            "Release Notes": {"rich_text": [{"text": {"content": _clip(data.get("release_notes", ""))}}]},
            "Post Monitoring": {"rich_text": [{"text": {"content": _clip(data.get("post_monitoring", ""))}}]},
            "Status": {"select": {"name": data.get("status", "진행중")}},
        },
    }


def create_ops_log_entry(**data: str) -> bool:
    payload = build_payload(**data)
    response = requests.post(NOTION_API_URL, headers=headers, json=payload)
    if response.status_code in {200, 201}:
        logging.info("✅ Notion DB에 성공적으로 기록되었습니다.")
        return True
    logging.error("❌ 기록 실패: %s %s", response.status_code, response.text)
    if SLACK_WEBHOOK_URL:
        try:
            requests.post(SLACK_WEBHOOK_URL, json={"text": f"Ops log 실패: {response.text}"})
        except Exception as exc:
            logging.warning("Slack 알림 실패: %s", exc)
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log operations to Notion")
    parser.add_argument("log_type")
    parser.add_argument("operator")
    parser.add_argument("module")
    parser.add_argument("environment")
    parser.add_argument("task_summary")
    parser.add_argument("action_details")
    parser.add_argument("--verification", default="")
    parser.add_argument("--error_summary", default="")
    parser.add_argument("--root_cause", default="")
    parser.add_argument("--resolution", default="")
    parser.add_argument("--patch_details", default="")
    parser.add_argument("--release_version", default="")
    parser.add_argument("--release_notes", default="")
    parser.add_argument("--post_monitoring", default="")
    parser.add_argument("--status", default="진행중")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    success = create_ops_log_entry(**vars(args))
    if not success:
        exit(1)
