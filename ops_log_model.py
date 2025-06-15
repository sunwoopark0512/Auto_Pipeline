from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class OpsLogModel:
    """Utility for building Notion payloads for operational logs."""

    log_type: str
    operator: str
    module: str
    environment: str
    task_summary: str
    action_details: str
    status: str
    error_summary: Optional[str] = None
    version: Optional[str] = None

    @classmethod
    def build_payload(
        cls,
        log_type: str,
        operator: str,
        module: str,
        environment: str,
        task_summary: str,
        action_details: str,
        status: str,
        error_summary: Optional[str] = None,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat() + "Z"
        return {
            "properties": {
                "로그유형": {"select": {"name": log_type}},
                "운영자": {"rich_text": [{"text": {"content": operator}}]},
                "모듈": {"title": [{"text": {"content": module}}]},
                "환경": {"select": {"name": environment}},
                "작업요약": {"rich_text": [{"text": {"content": task_summary}}]},
                "상세내역": {"rich_text": [{"text": {"content": action_details}}]},
                "상태": {"select": {"name": status}},
                "오류": {"rich_text": [{"text": {"content": error_summary or ""}}]},
                "버전": {"rich_text": [{"text": {"content": version or ""}}]},
                "발생일시": {"date": {"start": timestamp}},
            }
        }
