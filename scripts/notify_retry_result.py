"""Send Slack notification summarizing retry results."""

import os
import json
import logging
import urllib.request
from dotenv import load_dotenv

load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def load_result():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.info("결과 파일이 존재하지 않습니다: %s", REPARSED_OUTPUT_PATH)
        return 0, 0, 0
    with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    failed = len([d for d in data if d.get('retry_error')])
    success = total - failed
    return total, success, failed

def send_slack(total: int, success: int, failed: int) -> None:
    if not SLACK_WEBHOOK_URL:
        logging.warning("SLACK_WEBHOOK_URL가 설정되지 않아 슬랙 알림을 건너뜁니다.")
        return
    message = {
        "text": f"재업로드 결과\n총 시도: {total}\n성공: {success}\n실패: {failed}"
    }
    data = json.dumps(message).encode('utf-8')
    req = urllib.request.Request(SLACK_WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                logging.error("슬랙 전송 실패: %s", response.read().decode())
    except Exception as e:
        logging.error("슬랙 전송 중 예외 발생: %s", e)

def notify_retry_result():
    total, success, failed = load_result()
    send_slack(total, success, failed)
    logging.info("총 시도: %s, 성공: %s, 실패: %s", total, success, failed)

if __name__ == "__main__":
    notify_retry_result()
