import requests


def send_slack_message(webhook_url: str, message: str) -> None:
    payload = {"text": message}
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception:
        pass
