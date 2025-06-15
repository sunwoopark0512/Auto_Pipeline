import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")


def send_slack_alert(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        print("❌ Slack Webhook URL 미설정")
        return
    payload = {"text": message}
    res = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if res.status_code == 200:
        print("✅ Slack 알림 전송 완료")
    else:
        print(f"❌ Slack 전송 실패: {res.status_code}, {res.text}")
