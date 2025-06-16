import os
import json
import logging
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 결과 요약 ----------------------
def build_summary():
    if not os.path.exists(SUMMARY_PATH):
        return "재시도 결과 파일이 존재하지 않습니다."
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    failed = len([d for d in data if d.get('retry_error')])
    success = total - failed
    return f"재업로드 결과: 총 {total}건 중 {success}건 성공, {failed}건 실패"

# ---------------------- Slack 알림 ----------------------
def send_slack(message):
    if not WEBHOOK_URL:
        logging.warning("SLACK_WEBHOOK_URL 미설정으로 알림을 건너뜁니다.")
        return
    try:
        import requests
    except Exception as e:
        logging.error(f"requests 모듈 필요: {e}")
        return
    try:
        resp = requests.post(WEBHOOK_URL, json={'text': message})
        resp.raise_for_status()
        logging.info("📣 Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"Slack 전송 실패: {e}")

# ---------------------- 메인 ----------------------
def main():
    msg = build_summary()
    send_slack(msg)

if __name__ == '__main__':
    main()
