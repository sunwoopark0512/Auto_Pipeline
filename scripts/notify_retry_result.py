import os
import json
import logging
from dotenv import load_dotenv
import requests

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_summary():
    if not os.path.exists(SUMMARY_PATH):
        logging.info(f"❗ 요약 파일이 존재하지 않습니다: {SUMMARY_PATH}")
        return None
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    failed = len([i for i in data if i.get("retry_error")])
    success = total - failed
    return {"total": total, "success": success, "failed": failed}


def send_slack(summary):
    if not WEBHOOK_URL:
        logging.error("SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    msg = f"재업로드 결과: 성공 {summary['success']}개, 실패 {summary['failed']}개"
    try:
        response = requests.post(WEBHOOK_URL, json={"text": msg})
        if response.status_code != 200:
            logging.error(f"Slack 전송 실패: {response.status_code} {response.text}")
        else:
            logging.info("📣 Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 요청 중 오류: {e}")


def main():
    summary = load_summary()
    if summary is None:
        return
    send_slack(summary)


if __name__ == "__main__":
    main()

