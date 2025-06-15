import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 요약 파일이 없습니다: {SUMMARY_PATH}")
        return

    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed

    message = f"재업로드 결과: 전체 {total}개 중 성공 {success}개, 실패 {failed}개"
    logging.info(message)

    if SLACK_WEBHOOK_URL:
        try:
            import requests
            requests.post(SLACK_WEBHOOK_URL, json={"text": message})
            logging.info("📣 Slack 알림 전송 완료")
        except Exception as e:
            logging.warning(f"Slack 전송 실패: {e}")

if __name__ == "__main__":
    main()
