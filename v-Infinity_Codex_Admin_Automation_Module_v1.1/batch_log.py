import os
from notion_client import NotionClient
from ops_log_model import OpsLogModel

NOTION_TOKEN = os.getenv("NOTION_API_SECRET", "")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID", "")


def auto_deployment_log(module: str, env: str, version: str) -> None:
    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
    payload = OpsLogModel.build_payload(
        log_type="Deployment",
        operator="DeployBot",
        module=module,
        environment=env,
        task_summary="자동 배포 기록",
        action_details=f"배포 버전 {version} 자동 기록",
        release_version=version,
        status="완료",
    )

    res = notion.create_page(payload)
    if res.status_code in [200, 201]:
        print("✅ 배포 로그 자동 기록 성공")
    else:
        print("❌ 기록 실패:", res.status_code, res.text)
