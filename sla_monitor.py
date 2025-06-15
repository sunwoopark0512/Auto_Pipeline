from __future__ import annotations

import os
from notion_client_wrapper import NotionClient
from ops_log_model import OpsLogModel
from slack_alert import send_slack_alert

NOTION_TOKEN = os.getenv("NOTION_API_SECRET", "")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID", "")


def record_sla_issue(
    module: str, environment: str, error_summary: str, severity: str = "Major"
) -> None:
    """Record SLA issue to Notion and send Slack alert."""
    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
    payload = OpsLogModel.build_payload(
        log_type="Error",
        operator="AutoSLA",
        module=module,
        environment=environment,
        task_summary="SLA 장애 발생",
        action_details="자동 SLA 이슈 기록",
        error_summary=error_summary,
        status="오류 발생",
    )
    res = notion.create_page(payload)
    status_code = getattr(res, "status_code", 200)
    if status_code in (200, 201):
        print("✅ SLA 장애 기록 완료")
        send_slack_alert(f"🚨 SLA 장애 발생 [{severity}] - {module}: {error_summary}")
    else:
        print("❌ SLA 기록 실패:", status_code)
