import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
FAILED_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def summarize_results():
    if not os.path.exists(FAILED_PATH):
        return 0
    with open(FAILED_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return len(data)


def send_slack_message(text):
    if not WEBHOOK_URL:
        logging.error("❌ SLACK_WEBHOOK_URL 환경 변수가 없습니다.")
        return
    try:
        requests.post(WEBHOOK_URL, json={"text": text}, timeout=10)
        logging.info("📣 Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"❌ Slack 알림 실패: {e}")


def notify():
    remaining = summarize_results()
    if remaining == 0:
        message = "✅ Retry succeeded. No failed keywords remain."
    else:
        message = f"⚠️ Retry complete. {remaining} keywords still failed."
    send_slack_message(message)
    print(message)


if __name__ == "__main__":
    notify()
