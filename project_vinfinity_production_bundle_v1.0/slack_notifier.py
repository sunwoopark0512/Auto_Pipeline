"""Send notifications to Slack via webhook."""

import requests


def notify_slack(message: str, webhook: str) -> None:
    """Post a message to Slack."""
    try:
        requests.post(webhook, json={"text": message}, timeout=5)
    except requests.RequestException:
        pass
