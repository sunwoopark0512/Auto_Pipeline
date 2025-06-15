import os
import json
import logging
import requests
from dotenv import load_dotenv

# ---------------------- 설정 로딩 ----------------------
load_dotenv()
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 결과 로딩 ----------------------
def load_results():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 결과 파일이 없습니다: {SUMMARY_PATH}")
        return []
    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------- 통계 계산 ----------------------
def summarize_results(items):
    total = len(items)
    failed = len([i for i in items if i.get("retry_error")])
    success = total - failed
    return total, success, failed

# ---------------------- 슬랙 알림 전송 ----------------------
def send_slack(total, success, failed):
    if not SLACK_WEBHOOK_URL:
        logging.error("❌ SLACK_WEBHOOK_URL 환경 변수가 누락되었습니다.")
        return

    message = {
        "text": "\n".join([
            "*\ud83d\udcca \uc7ac\uc2dc\ub3c4 \uacb0\uacfc \uc694\uc57d*",
            f"- \ucd1d \ud56d\ubaa9: {total}",
            f"- \uc131\uacf5: {success}",
            f"- \uc2e4\ud328 \uc720\uc9c0: {failed}",
        ])
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=10)
        response.raise_for_status()
        logging.info("\u2705 Slack \uc54c\ub9bc \uc804\uc1a1 \uc644\ub8cc")
    except Exception as e:
        logging.error(f"\u274c Slack \uc804\uc1a1 \uc2e4\ud328: {e}")

# ---------------------- main ----------------------
def main():
    items = load_results()
    total, success, failed = summarize_results(items)
    logging.info(f"\ud83d\udce6 \uc7ac\uc2dc\ub3c4 \uacb0\uacfc - \uc131\uacf5 {success} / \uc2e4\ud328 {failed} / \ucd1d {total}")
    send_slack(total, success, failed)

if __name__ == "__main__":
    main()
