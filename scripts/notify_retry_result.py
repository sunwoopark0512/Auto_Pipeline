import os
import json
import logging
import urllib.request
from dotenv import load_dotenv

load_dotenv()
WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_PATH = os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_summary():
    if not os.path.exists(SUMMARY_PATH):
        logging.error(f"❌ 요약 파일이 없습니다: {SUMMARY_PATH}")
        return None
    with open(SUMMARY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    failed = len([d for d in data if d.get("retry_error")])
    success = total - failed
    rate = round((success / total) * 100, 1) if total > 0 else 0.0
    return {"total": total, "success": success, "failed": failed, "rate": rate}


def send_slack(summary):
    if not WEBHOOK:
        logging.error("❗ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return
    text = (
        f"재시도 결과 보고\n"
        f"전체: {summary['total']}\n"
        f"성공: {summary['success']} 실패: {summary['failed']}\n"
        f"성공률: {summary['rate']}%"
    )
    payload = json.dumps({"text": text}).encode('utf-8')
    req = urllib.request.Request(WEBHOOK, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            resp.read()
        logging.info("📨 슬랙 알림 전송 완료")
    except Exception as e:
        logging.error(f"❌ 슬랙 전송 실패: {e}")


if __name__ == "__main__":
    summary = load_summary()
    if summary:
        logging.info(f"📊 재시도 요약: {summary}")
        send_slack(summary)
