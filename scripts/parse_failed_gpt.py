from utils.logging_util import get_logger

logger = get_logger("parse_failed_gpt")


def parse(log_path: str) -> dict:
    logger.info("파싱 스텁 – %s", log_path)
    return {"status": "parsed"}


if __name__ == "__main__":
    import sys
    import json
    print(json.dumps(parse(sys.argv[1] if len(sys.argv) > 1 else "log.txt")))
