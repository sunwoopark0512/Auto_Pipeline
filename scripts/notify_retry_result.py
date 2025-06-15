import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
RESULT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

def load_results():
    if not os.path.exists(RESULT_PATH):
        logging.warning(f"❗ 결과 파일이 존재하지 않습니다: {RESULT_PATH}")
        return []
    try:
        with open(RESULT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"❌ 결과 파일 읽기 오류: {e}")
        return []

def notify():
    results = load_results()
    total = len(results)
    failed = len([r for r in results if r.get("retry_error")])
    success = total - failed

    message = f"재업로드 결과: 총 {total}개 중 {success}개 성공, {failed}개 실패"

    if not WEBHOOK_URL:
        logging.info(message)
        logging.warning("SLACK_WEBHOOK_URL 미설정, 콘솔에만 출력")
        return

    try:
        requests.post(WEBHOOK_URL, json={"text": message}, timeout=10)
        logging.info("✅ Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"❌ Slack 알림 실패: {e}")

if __name__ == "__main__":
    notify()
