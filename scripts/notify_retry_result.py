import os
import json
import logging
import requests
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 요약 데이터 로딩 ----------------------
def load_retry_data():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.error(f"❌ 요약 파일을 찾을 수 없습니다: {REPARSED_OUTPUT_PATH}")
        return None
    try:
        with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"❌ 요약 파일 읽기 오류: {e}")
        return None

# ---------------------- 성공/실패 집계 ----------------------
def summarize(data):
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    return success, failed

# ---------------------- 슬랙 알림 전송 ----------------------
def notify_slack(success, failed):
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    message = f"재시도 결과\n✅ 성공: {success}개\n❌ 실패 유지: {failed}개"
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        if response.status_code == 200:
            logging.info("📣 Slack 알림 전송 완료")
        else:
            logging.error(f"❌ Slack 전송 실패: {response.status_code} {response.text}")
    except Exception as e:
        logging.error(f"❌ Slack 요청 오류: {e}")

# ---------------------- 실행 진입점 ----------------------
if __name__ == "__main__":
    data = load_retry_data()
    if data is not None:
        success, failed = summarize(data)
        logging.info(f"📦 재시도 요약 - 성공: {success}, 실패 유지: {failed}")
        notify_slack(success, failed)
