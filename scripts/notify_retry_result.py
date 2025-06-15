import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def load_summary():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 결과 파일이 없습니다: {SUMMARY_PATH}")
        return None
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def send_slack(text: str):
    if not WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    try:
        resp = requests.post(WEBHOOK_URL, json={"text": text})
        resp.raise_for_status()
        logging.info("📢 Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"❌ Slack 전송 실패: {e}")

def main():
    data = load_summary()
    if data is None:
        return
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed

    message = f"재시도 결과\n총 시도: {total}\n성공: {success}\n실패: {failed}"
    send_slack(message)

if __name__ == "__main__":
    main()
