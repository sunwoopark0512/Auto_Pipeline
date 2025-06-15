import os
import argparse
from notion_client import NotionClient
from ops_log_model import OpsLogModel
from slack_alert import send_slack_alert

NOTION_TOKEN = os.getenv("NOTION_API_SECRET", "")
NOTION_DB_ID = os.getenv("NOTION_DATABASE_ID", "")


def register_log(args: argparse.Namespace) -> None:
    notion = NotionClient(NOTION_TOKEN, NOTION_DB_ID)

    payload = OpsLogModel.build_payload(
        log_type=args.log_type,
        operator=args.operator,
        module=args.module,
        environment=args.environment,
        task_summary=args.task_summary,
        action_details=args.action_details,
        verification=args.verification,
        error_summary=args.error_summary,
        root_cause=args.root_cause,
        resolution=args.resolution,
        patch_details=args.patch_details,
        release_version=args.release_version,
        release_notes=args.release_notes,
        post_monitoring=args.post_monitoring,
        status=args.status,
    )

    res = notion.create_page(payload)
    if res.status_code in [200, 201]:
        print("✅ Notion 기록 성공")
        send_slack_alert(f"[v-Infinity Log] {args.log_type} 등록 완료: {args.task_summary}")
    else:
        print("❌ 기록 실패:", res.status_code, res.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_type", required=True)
    parser.add_argument("--operator", required=True)
    parser.add_argument("--module", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--task_summary", required=True)
    parser.add_argument("--action_details", required=True)
    parser.add_argument("--verification", default="")
    parser.add_argument("--error_summary", default="")
    parser.add_argument("--root_cause", default="")
    parser.add_argument("--resolution", default="")
    parser.add_argument("--patch_details", default="")
    parser.add_argument("--release_version", default="")
    parser.add_argument("--release_notes", default="")
    parser.add_argument("--post_monitoring", default="")
    parser.add_argument("--status", default="진행중")

    args = parser.parse_args()
    register_log(args)
