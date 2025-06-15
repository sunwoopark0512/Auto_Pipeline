import os
import json
import logging
from dotenv import load_dotenv
import requests

load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def build_summary():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.warning(f"재시도 결과 파일이 없습니다: {REPARSED_OUTPUT_PATH}")
        return "재시도 결과 파일이 존재하지 않습니다."

    with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    return f"총 시도: {total}\n성공: {success}\n실패: {failed}"

def send_slack(message: str):
    if not SLACK_WEBHOOK_URL:
        logging.info("SLACK_WEBHOOK_URL이 설정되지 않아 출력만 진행합니다.")
        print(message)
        return
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if response.status_code == 200:
            logging.info("슬랙 알림 전송 성공")
        else:
            logging.error(f"슬랙 전송 실패: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"슬랙 요청 실패: {e}")

if __name__ == "__main__":
    summary = build_summary()
    send_slack(summary)
