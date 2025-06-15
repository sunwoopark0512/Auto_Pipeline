import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

FAILED_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def notify():
    remaining = 0
    if os.path.exists(FAILED_PATH):
        try:
            with open(FAILED_PATH, 'r', encoding='utf-8') as f:
                remaining = len(json.load(f))
        except Exception as e:
            logging.warning(f"파일 읽기 오류: {e}")

    message = f"Notion retry finished. Remaining failures: {remaining}"
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"text": message})
            logging.info("Slack 알림 전송 완료")
        except Exception as e:
            logging.error(f"Slack 전송 실패: {e}")
    else:
        logging.info(message)

if __name__ == "__main__":
    notify()
