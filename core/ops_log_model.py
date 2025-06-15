import datetime

class OpsLogModel:
    """Minimal stub for OpsLogModel used in tests."""

    @staticmethod
    def build_payload(
        log_type: str,
        operator: str,
        module: str,
        environment: str,
        task_summary: str,
        action_details: str,
    ) -> dict:
        now = datetime.datetime.utcnow().isoformat()
        return {
            "parent": {"database_id": "DUMMY"},
            "properties": {
                "Log Type": {"select": {"name": log_type}},
                "Date": {"date": {"start": now}},
                "Operator": {"title": [{"text": {"content": operator}}]},
                "Module": {"rich_text": [{"text": {"content": module}}]},
                "Environment": {"select": {"name": environment}},
                "Task Summary": {"rich_text": [{"text": {"content": task_summary}}]},
                "Action Details": {"rich_text": [{"text": {"content": action_details}}]},
            },
        }
