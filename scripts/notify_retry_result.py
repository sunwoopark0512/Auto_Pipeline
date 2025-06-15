import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def notify_retry_result():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.info(f"❌ 재시도 결과 파일이 존재하지 않습니다: {REPARSED_OUTPUT_PATH}")
        return

    with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    message = f"재업로드 결과: 성공 {success}, 실패 {failed}"

    if SLACK_WEBHOOK_URL:
        try:
            requests.post(SLACK_WEBHOOK_URL, json={"text": message})
            logging.info("✅ Slack 알림 전송 완료")
        except Exception as e:
            logging.error(f"❌ Slack 알림 실패: {e}")
    else:
        print(message)


if __name__ == "__main__":
    notify_retry_result()
