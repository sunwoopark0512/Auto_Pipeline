import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def notify_result():
    if not os.path.exists(SUMMARY_PATH):
        logging.warning(f"❗ 결과 파일이 존재하지 않습니다: {SUMMARY_PATH}")
        return

    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    failed = len([d for d in data if d.get('retry_error')])
    success = total - failed

    message = f"재업로드 결과\n총 시도: {total}\n성공: {success}\n실패: {failed}"

    if WEBHOOK_URL:
        try:
            response = requests.post(WEBHOOK_URL, json={'text': message})
            if response.status_code == 200:
                logging.info("✅ Slack 알림 전송 완료")
            else:
                logging.error(f"❌ Slack 응답 오류: {response.status_code} {response.text}")
        except Exception as e:
            logging.error(f"❌ Slack 알림 전송 실패: {e}")
    else:
        logging.info("SLACK_WEBHOOK_URL 미설정. 다음 메시지 출력:\n" + message)


if __name__ == "__main__":
    notify_result()
