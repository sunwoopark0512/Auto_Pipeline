import os
from notion_client import NotionClient
from ops_log_model import OpsLogModel
from slack_alert import send_slack_alert

NOTION_TOKEN = os.getenv("NOTION_API_SECRET")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID")

def record_sla_issue(module, environment, error_summary, severity="Major"):
    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
    payload = OpsLogModel.build_payload(
        log_type="Error",
        operator="AutoSLA",
        module=module,
        environment=environment,
        task_summary="SLA 장애 발생",
        action_details="자동 SLA 이슈 기록",
        error_summary=error_summary,
        status="오류 발생"
    )
    res = notion.create_page(payload)
    if res.status_code in [200, 201]:
        print("✅ SLA 장애 기록 완료")
        send_slack_alert(f"🚨 SLA 장애 발생 [{severity}] - {module}: {error_summary}")
    else:
        print("❌ SLA 기록 실패:", res.status_code, res.text)
