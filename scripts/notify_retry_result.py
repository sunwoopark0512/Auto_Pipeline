"""
stdin 으로 받은 재시도 결과(summary JSON)를 Slack Webhook으로 전송.
"""
import json
import os
import sys

import requests

HOOK = os.getenv("SLACK_WEBHOOK", "")

def notify(summary: dict):
    if not HOOK:
        print("⚠️  SLACK_WEBHOOK 미설정 – 알림 생략")
        return
    text = json.dumps(summary, indent=2, ensure_ascii=False)
    requests.post(HOOK, json={"text": f"✅ GPT 재시도 결과\n```{text}```"})


if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    notify(payload)
