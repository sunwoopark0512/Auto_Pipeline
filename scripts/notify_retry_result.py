import os
import json
import logging
from dotenv import load_dotenv
import requests

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_retry_results():
    """Load parsed retry results from JSON file."""
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        logging.error(f"❌ 결과 파일을 찾을 수 없습니다: {REPARSED_OUTPUT_PATH}")
        return None
    try:
        with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as exc:
        logging.error(f"❌ 결과 파일 읽기 오류: {exc}")
        return None


def summarize_results(data):
    """Return count of successes and failures from retry data."""
    if not isinstance(data, list):
        logging.error("❌ 잘못된 데이터 형식: 리스트가 필요합니다")
        return None
    failed = len([d for d in data if d.get("retry_error")])
    success = len(data) - failed
    return success, failed


def post_to_slack(success, failed):
    """Send summary message to Slack."""
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다")
        return

    message = f"재시도 결과 보고\n성공: {success}개\n실패 지속: {failed}개"
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        if response.status_code == 200:
            logging.info("✅ Slack 알림 전송 성공")
        else:
            logging.error(f"❌ Slack 알림 실패: {response.status_code} {response.text}")
    except Exception as exc:
        logging.error(f"❌ Slack 요청 중 오류: {exc}")


if __name__ == "__main__":
    results = load_retry_results()
    if results is not None:
        summary = summarize_results(results)
        if summary:
            s, f = summary
            logging.info(f"📋 재시도 결과 - 성공: {s}, 실패 지속: {f}")
            post_to_slack(s, f)
