import os
import json
import logging
from dotenv import load_dotenv
import requests

# ---------------------- 환경 변수 로딩 ----------------------
load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 결과 로딩 ----------------------
def load_retry_results():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.error(f"❌ 결과 파일이 없습니다: {REPARSED_OUTPUT_PATH}")
        return []
    try:
        with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"❌ 결과 파일 읽기 실패: {e}")
        return []

# ---------------------- 통계 계산 ----------------------
def summarize_results(data):
    total = len(data)
    failed = len([item for item in data if item.get("retry_error")])
    success = total - failed
    return success, failed

# ---------------------- Slack 알림 전송 ----------------------
def send_slack_message(success, failed):
    if not SLACK_WEBHOOK_URL:
        logging.error("❌ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return

    message = f"🔄 키워드 재업로드 결과\n✅ 성공: {success}개\n❌ 실패 유지: {failed}개"
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        response.raise_for_status()
        logging.info("📨 Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"❌ Slack 전송 실패: {e}")

# ---------------------- 메인 ----------------------
if __name__ == "__main__":
    results = load_retry_results()
    if not results:
        logging.info("✅ 재시도 결과가 없습니다.")
    success, failed = summarize_results(results)
    logging.info(f"📦 재시도 결과 요약 - 성공: {success}, 실패: {failed}")
    send_slack_message(success, failed)
