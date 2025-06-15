"""Command-line entry point for logging operational events to Notion."""

import os

from notion_client import NotionClient
from ops_log_model import OpsLogModel


NOTION_TOKEN = os.getenv("NOTION_API_SECRET", "")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID", "")


def register_log() -> None:
    """Example function to register an operations log."""
    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)

    payload = OpsLogModel.build_payload(
        log_type="DevOps",
        operator="Sunwoo",
        module="ExportScript",
        environment="Local",
        task_summary="Full Export 테스트",
        action_details="폴더 생성 및 검증 완료",
        database_id=NOTION_DB_ID,
    )

    res = notion.create_page(payload)
    if res.status_code in (200, 201):
        print("✅ 성공적으로 기록됨")
    else:
        print("❌ 기록 실패:", res.status_code, res.text)


if __name__ == "__main__":
    register_log()
