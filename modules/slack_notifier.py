"""Send notifications to Slack webhooks."""

import requests


def send_slack_message(webhook_url: str, message: str):
    """Send a simple text payload to a Slack webhook."""

    payload = {"text": message}
    response = requests.post(webhook_url, json=payload, timeout=10)
    return response.status_code
