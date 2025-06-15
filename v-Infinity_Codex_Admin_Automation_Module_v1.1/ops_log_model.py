class OpsLogModel:
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
    ) -> dict:
        def title(value: str) -> dict:
            return {"title": [{"text": {"content": value}}]}

        def rich(value: str) -> dict:
            return {"rich_text": [{"text": {"content": value}}]}

        properties = {
            "Log Type": title(log_type),
            "Operator": rich(operator),
            "Module": rich(module),
            "Environment": rich(environment),
            "Task Summary": rich(task_summary),
            "Action Details": rich(action_details),
            "Verification": rich(verification),
            "Error Summary": rich(error_summary),
            "Root Cause": rich(root_cause),
            "Resolution": rich(resolution),
            "Patch Details": rich(patch_details),
            "Release Version": rich(release_version),
            "Release Notes": rich(release_notes),
            "Post Monitoring": rich(post_monitoring),
            "Status": rich(status),
        }
        return properties
