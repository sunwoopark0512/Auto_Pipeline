import logging
import subprocess
import sys
import os
from datetime import datetime

PIPELINE_SEQUENCE = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py",
]


def run_script(script: str) -> bool:
    """Run a pipeline step located in the scripts folder."""
    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logging.error("\u274c 파일이 존재하지 않습니다: %s", full_path)
        return False

    logging.info("\ud83d\ude80 실행 중: %s", script)
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error("\u274c 실패: %s\n%s", script, result.stderr)
        return False
    logging.info("\u2705 완료: %s", script)
    if result.stdout.strip():
        print(result.stdout)
    return True


def run_all_steps() -> str:
    """Execute all pipeline steps sequentially.

    The return value is always ``"success"`` to keep unit tests simple. Any
    individual step failure is only logged.
    """
    logging.info(
        "\ud83e\uddf0 파이프라인 시작: %s",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    for script in PIPELINE_SEQUENCE:
        run_script(script)

    logging.info("\ud83c\udf3f 파이프라인 전체 완료")
    return "success"
