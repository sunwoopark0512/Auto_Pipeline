import os
import json
import logging
import urllib.request
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
REPARSED_OUTPUT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def send_slack_message(text: str):
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    data = json.dumps({"text": text}).encode('utf-8')
    req = urllib.request.Request(SLACK_WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                logging.error(f"❌ Slack 전송 실패: HTTP {resp.status}")
            else:
                logging.info("✅ Slack 알림 전송 완료")
    except Exception as e:
        logging.error(f"❌ Slack 요청 오류: {e}")


def notify_retry_result():
    if not os.path.exists(REPARSED_OUTPUT_PATH):
        send_slack_message("✅ 모든 키워드가 성공적으로 업로드되었습니다.")
        return

    try:
        with open(REPARSED_OUTPUT_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logging.error(f"❌ 결과 파일 읽기 오류: {e}")
        return

    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    message = f"재시도 결과 - 성공: {success}, 실패: {failed}"
    send_slack_message(message)


if __name__ == "__main__":
    notify_retry_result()
