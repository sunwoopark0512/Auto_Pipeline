"""Utility for sending Slack notifications."""

import os
import sys
import requests


def send_slack_message(webhook_url: str, message: str) -> int:
    """Send a message to Slack via an incoming webhook."""
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload, timeout=10)
    return response.status_code


def main() -> None:
    """Send a message provided via command line arguments."""
    url = os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        raise SystemExit("SLACK_WEBHOOK_URL environment variable is not set")

    message = " ".join(sys.argv[1:]) or "Pipeline notification"
    status = send_slack_message(url, message)
    print(f"Slack response status: {status}")


if __name__ == "__main__":
    main()
