import os
import json
import logging
from dotenv import load_dotenv
import requests

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def notify_result():
    if not os.path.exists(SUMMARY_PATH):
        logging.warning(f"\u2757\ufe0f 요약 파일이 없습니다: {SUMMARY_PATH}")
        return
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    message = f"재시도 결과: 총 {total}건 중 {success}건 성공, {failed}건 실패"

    if WEBHOOK_URL:
        try:
            resp = requests.post(WEBHOOK_URL, json={"text": message})
            if resp.status_code == 200:
                logging.info("\uD83D\uDCE2 Slack 알림 전송 완료")
            else:
                logging.error(f"Slack 응답 오류: {resp.text}")
        except Exception as e:
            logging.error(f"Slack 전송 실패: {e}")
    else:
        logging.info(message)

if __name__ == "__main__":
    notify_result()
