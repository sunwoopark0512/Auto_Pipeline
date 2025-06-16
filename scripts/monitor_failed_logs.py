import os
import json
import logging
import subprocess
import sys
from glob import glob
from datetime import datetime
from dotenv import load_dotenv
import requests

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
LOG_DIR = os.getenv("LOG_DIR", "logs")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
RETRY_SCRIPT = os.getenv("RETRY_SCRIPT", "scripts/retry_failed_uploads.py")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 실패 로그 탐색 ----------------------
def find_failed_files():
    pattern = os.path.join(LOG_DIR, "failed_*")
    return [f for f in glob(pattern) if os.path.isfile(f)]

# ---------------------- Slack 알림 ----------------------
def send_slack(text):
    if not SLACK_WEBHOOK_URL:
        logging.info("Slack webhook URL 미설정, 알림 건너뜀")
        return
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": text})
        if resp.status_code != 200:
            logging.warning(f"Slack 전송 실패: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.error(f"Slack 전송 예외: {e}")

# ---------------------- 모니터링 및 재시도 ----------------------
def monitor_and_retry():
    failed_files = find_failed_files()
    if not failed_files:
        logging.info("✅ 실패 로그 파일 없음")
        return

    summary_lines = []
    for path in failed_files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            count = len(data) if isinstance(data, list) else 0
        except Exception:
            count = 0
        summary_lines.append(f"{os.path.basename(path)}: {count}")
    summary = "\n".join(summary_lines)

    message = f"[AutoPipeline] 실패 감지 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n" + summary
    logging.info(message)
    send_slack(message)

    if os.path.exists(RETRY_SCRIPT):
        logging.info(f"재시도 스크립트 실행: {RETRY_SCRIPT}")
        subprocess.call([sys.executable, RETRY_SCRIPT])
    else:
        logging.warning(f"재시도 스크립트를 찾을 수 없습니다: {RETRY_SCRIPT}")

if __name__ == "__main__":
    monitor_and_retry()
