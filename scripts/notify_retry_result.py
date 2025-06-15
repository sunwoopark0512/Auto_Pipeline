"""Slack notification for retry results."""

import os
import json
import logging
from dotenv import load_dotenv
import requests

load_dotenv()

RESULT_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def load_results(path: str):
    """Load retry results from ``path``."""
    if not os.path.exists(path):
        logging.error("\u274c 결과 파일을 찾을 수 없습니다: %s", path)
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as exc:
        logging.error("\u274c 결과 파일을 읽는 중 오류 발생: %s", exc)
        return []


def summarize_results(items):
    """Return a formatted summary for ``items``."""
    if not items:
        return "재시도 대상이 없습니다."
    total = len(items)
    still_failed = len([it for it in items if it.get("retry_error")])
    success = total - still_failed
    return (
        "📦 재시도 결과 요약\n"
        f"총 항목: {total}\n"
        f"✅ 성공: {success}\n"
        f"❌ 실패 유지: {still_failed}"
    )


def send_to_slack(text: str):
    """Post ``text`` to Slack."""
    if not SLACK_WEBHOOK_URL:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return False
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=10)
        if resp.status_code != 200:
            logging.error("\u274c 슬랙 전송 실패: %s %s", resp.status_code, resp.text)
            return False
        logging.info("✅ 슬랙 알림 전송 완료")
        return True
    except Exception as exc:
        logging.error("\u274c 슬랙 전송 중 오류: %s", exc)
        return False


def main():
    """Entry point for CLI execution."""
    items = load_results(RESULT_PATH)
    summary = summarize_results(items)
    logging.info(summary)
    send_to_slack(summary)


if __name__ == "__main__":
    main()
