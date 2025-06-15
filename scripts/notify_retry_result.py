from utils.logging_util import get_logger

logger = get_logger("notify_retry")


def send(message: str) -> None:
    # TODO: Slack 또는 이메일 통합
    logger.info("알림 발송 스텁: %s", message)


if __name__ == "__main__":
    import sys
    send(" ".join(sys.argv[1:]) or "테스트 알림")
