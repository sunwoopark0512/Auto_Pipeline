import os
import json
import logging
import requests


def notify_retry_result():
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    summary_path = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    if not webhook_url:
        logging.error("SLACK_WEBHOOK_URL 환경 변수가 없습니다.")
        return
    if not os.path.exists(summary_path):
        logging.warning(f"요약 파일을 찾을 수 없습니다: {summary_path}")
        return
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        text = f"Retry summary: {len(data)} items"
        requests.post(webhook_url, json={"text": text})
        logging.info("Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 알림 실패: {e}")


if __name__ == "__main__":
    notify_retry_result()
