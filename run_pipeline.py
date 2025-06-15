import logging
from notifier import send_slack_notification
from src.pipeline import run_all_steps

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    try:
        send_slack_notification("Pipeline 시작")
        result = run_all_steps()
        send_slack_notification(f"Pipeline 완료: {result}")
    except Exception as exc:
        logger.error("Pipeline failed: %s", exc, exc_info=True)
        send_slack_notification(f"Pipeline 실패: {exc}")
