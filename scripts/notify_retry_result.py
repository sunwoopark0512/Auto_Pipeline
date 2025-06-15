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
        logging.warning(f"❗ 요약 파일이 없습니다: {SUMMARY_PATH}")
        return []
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def send_slack(total: int, success: int, failed: int):
    if not WEBHOOK_URL:
        logging.error("SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    text = f"재업로드 결과 - 총 {total}개 중 성공 {success}개, 실패 {failed}개"
    try:
        resp = requests.post(WEBHOOK_URL, json={"text": text})
        if resp.status_code != 200:
            logging.error(f"Slack 응답 오류: {resp.status_code} {resp.text}")
        else:
            logging.info("Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 전송 실패: {e}")


def notify_retry_result():
    data = load_summary()
    if not data:
        logging.info("요약할 데이터가 없습니다.")
        return

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed

    send_slack(total, success, failed)


if __name__ == "__main__":
    notify_retry_result()
