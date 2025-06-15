"""
공통 재시도 로직.

사용:
    python -m scripts.retry run_pipeline.py 3
"""
import subprocess
import sys
import time
import pathlib

from utils.logging_util import get_logger

logger = get_logger("retry")


def run(cmd: list[str], retries: int = 3, delay: int = 5) -> int:
    for attempt in range(1, retries + 1):
        logger.info("실행 %s/%s: %s", attempt, retries, " ".join(cmd))
        res = subprocess.run(cmd)
        if res.returncode == 0:
            logger.info("성공!")
            return 0
        logger.warning("실패 코드 %s, %ss 후 재시도", res.returncode, delay)
        time.sleep(delay)
    return res.returncode


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: retry.py <script> [retries]")
        sys.exit(1)
    script = pathlib.Path(sys.argv[1])
    retries = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    sys.exit(run([sys.executable, str(script)], retries=retries))
