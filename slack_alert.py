from __future__ import annotations

import os
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(message: str) -> object:
    """Send a message to Slack via an incoming webhook."""
    if not SLACK_WEBHOOK_URL:
        print("⚠️ Slack webhook URL not configured")
        return None

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=5)
        return response
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Slack alert failed: {exc}")
        return None
