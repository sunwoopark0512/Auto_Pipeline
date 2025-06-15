"""Model helpers for constructing operation log payloads."""

from __future__ import annotations

import datetime
from typing import Any, Dict


class OpsLogModel:
    """Utility for building standardized Notion payloads."""

    @staticmethod
    def build_payload(
        log_type: str,
        operator: str,
        module: str,
        environment: str,
        task_summary: str,
        action_details: str,
        verification: str = "",
        error_summary: str = "",
        root_cause: str = "",
        resolution: str = "",
        patch_details: str = "",
        release_version: str = "",
        release_notes: str = "",
        post_monitoring: str = "",
        status: str = "진행중",
        database_id: str | None = None,
    ) -> Dict[str, Any]:
        """Construct a Notion page creation payload."""

        if not database_id:
            database_id = "YOUR_NOTION_DATABASE_ID"

        payload: Dict[str, Any] = {
            "parent": {"database_id": database_id},
            "properties": {
                "Log Type": {"select": {"name": log_type}},
                "Date": {"date": {"start": datetime.datetime.now().isoformat()}},
                "Operator": {"title": [{"text": {"content": operator}}]},
                "Module": {"rich_text": [{"text": {"content": module}}]},
                "Environment": {"select": {"name": environment}},
                "Task Summary": {"rich_text": [{"text": {"content": task_summary}}]},
                "Action Details": {"rich_text": [{"text": {"content": action_details}}]},
                "Verification": {"rich_text": [{"text": {"content": verification}}]},
                "Error Summary": {"rich_text": [{"text": {"content": error_summary}}]},
                "Root Cause": {"rich_text": [{"text": {"content": root_cause}}]},
                "Resolution": {"rich_text": [{"text": {"content": resolution}}]},
                "Patch Details": {"rich_text": [{"text": {"content": patch_details}}]},
                "Release Version": {"rich_text": [{"text": {"content": release_version}}]},
                "Release Notes": {"rich_text": [{"text": {"content": release_notes}}]},
                "Post Monitoring": {"rich_text": [{"text": {"content": post_monitoring}}]},
                "Status": {"select": {"name": status}},
            },
        }
        return payload
