import datetime

class OpsLogModel:
    @staticmethod
    def build_payload(
        log_type, operator, module, environment, task_summary,
        action_details, verification="", error_summary="", root_cause="",
        resolution="", patch_details="", release_version="", release_notes="",
        post_monitoring="", status="진행중"
    ):
        payload = {
            "parent": {"database_id": "YOUR_NOTION_DATABASE_ID"},
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
                "Status": {"select": {"name": status}}
            }
        }
        return payload
