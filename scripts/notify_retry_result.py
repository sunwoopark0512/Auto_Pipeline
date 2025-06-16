import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_summary():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 요약 파일이 없습니다: {SUMMARY_PATH}")
        return []
    try:
        with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"요약 파일 로딩 실패: {e}")
        return []


def send_slack_message(text: str):
    if not SLACK_WEBHOOK_URL:
        logging.info(text)
        return
    try:
        import requests
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": text})
        response.raise_for_status()
        logging.info("Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 전송 실패: {e}")


def main():
    items = load_summary()
    failed_count = len(items)
    message = f"🔁 재시도 결과 보고 - 남은 실패 항목: {failed_count}개"
    send_slack_message(message)


if __name__ == "__main__":
    main()
