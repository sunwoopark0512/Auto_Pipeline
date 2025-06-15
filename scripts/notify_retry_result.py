import os
import json
import logging
from dotenv import load_dotenv
import requests

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 요약 데이터 로딩 ----------------------
def load_retry_data():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 요약 파일이 존재하지 않습니다: {SUMMARY_PATH}")
        return None
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# ---------------------- 슬랙 메시지 전송 ----------------------
def send_slack_message(success: int, failed: int):
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
        return False
    total = success + failed
    text = f"재시도 결과 보고\n총 {total}건 중 {success}건 성공, {failed}건 실패"
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=10)
        resp.raise_for_status()
        logging.info("✅ Slack 메시지 전송 성공")
        return True
    except Exception as e:
        logging.error(f"❌ Slack 메시지 전송 실패: {e}")
        return False

# ---------------------- 실행 진입점 ----------------------
if __name__ == "__main__":
    data = load_retry_data()
    if data is None:
        exit(1)
    failed_count = len([d for d in data if d.get("retry_error")])
    success_count = len(data) - failed_count
    logging.info(f"📊 재시도 성공 {success_count}건 / 실패 {failed_count}건")
    send_slack_message(success_count, failed_count)
