# -------------------- filename: self_healing_monitor.py --------------------
"""Monitor key modules and log results to Supabase with optional Slack alerts."""

import os
import time
import logging
import subprocess
from datetime import datetime, timezone

from slack_sdk.webhook import WebhookClient
from supabase import create_client

# ────────────── ENV ────────────── #
SLACK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
MONITOR_TABLE = "execution_log"

CHECK_INTERVAL = 60 * 15  # 15 minutes

MONITORED_COMMANDS = [
    ("orchestrator", "python orchestrator.py"),
    ("notion_sync", "python notion_sync.py --table content --limit 50"),
    ("strategy_optimizer", "python strategy_optimizer.py --table content --days 30"),
]

slack = WebhookClient(SLACK_URL) if SLACK_URL else None


def _get_supa():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def log_result(module: str, status: str, error: str = ""):
    """Insert execution result into Supabase."""
    record = {
        "module": module,
        "status": status,
        "error_message": error or None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _get_supa().table(MONITOR_TABLE).insert(record).execute()


def notify_slack(module: str, status: str, error: str = ""):
    """Send Slack notification if webhook configured."""
    if not slack:
        return
    emoji = "✅" if status == "success" else "❌"
    slack.send(
        text=f"{emoji} `{module}` 모듈 상태: *{status.upper()}*\n{error or ''}",
        username="Self-Healing Monitor",
    )


def run_and_monitor():
    for name, cmd in MONITORED_COMMANDS:
        logging.info("🔍 [%s] 실행 중: %s", name, cmd)
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=300)
            if result.returncode == 0:
                log_result(name, "success")
                notify_slack(name, "success")
            else:
                error_msg = result.stderr.decode()[:500]
                log_result(name, "fail", error_msg)
                notify_slack(name, "fail", error_msg)
        except Exception as exc:  # pylint: disable=broad-except
            log_result(name, "fail", str(exc))
            notify_slack(name, "fail", str(exc))


def loop_monitor():
    logging.info("=== 🩺 Self-Healing Monitor 시작 ===")
    while True:
        run_and_monitor()
        logging.info("⏱️ %ss 후 재검사", CHECK_INTERVAL)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop_monitor()
