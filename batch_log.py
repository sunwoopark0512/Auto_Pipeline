from __future__ import annotations

import os
from notion_client_wrapper import NotionClient
from ops_log_model import OpsLogModel

NOTION_TOKEN = os.getenv("NOTION_API_SECRET", "")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID", "")


def auto_deployment_log(module: str, environment: str, version: str) -> object:
    """Record deployment information to Notion."""
    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)
    payload = OpsLogModel.build_payload(
        log_type="Deploy",
        operator="AutoDeploy",
        module=module,
        environment=environment,
        task_summary="배포 기록",
        action_details=f"버전 {version} 배포",
        status="성공",
        version=version,
    )
    return notion.create_page(payload)
