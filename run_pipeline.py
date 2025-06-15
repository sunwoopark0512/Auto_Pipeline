from utils.logging_util import get_logger
from utils.env_util import require_vars
from scripts.parse_failed_gpt import parse
from scripts.notify_retry_result import send

import subprocess
import sys
import os
from datetime import datetime

logger = get_logger("pipeline")

PIPELINE_SEQUENCE = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py",
]


def run_script(script: str) -> bool:
    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logger.error("❌ 파일이 존재하지 않습니다: %s", full_path)
        return False

    logger.info("🚀 실행 중: %s", script)
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)

    if result.returncode != 0:
        logger.error("❌ 실패: %s\n%s", script, result.stderr)
        return False
    logger.info("✅ 완료: %s", script)
    if result.stdout.strip():
        print(result.stdout)
    return True


def main() -> None:
    require_vars(["NOTION_API_SECRET"])
    logger.info("🧩 파이프라인 시작: %s", datetime.now().strftime("%Y-%m-%d %H:%M"))
    all_passed = True

    for script in PIPELINE_SEQUENCE:
        success = run_script(script)
        if not success:
            all_passed = False

    logger.info("🎯 파이프라인 전체 완료")
    if all_passed:
        logger.info("✅ 모든 단계 성공적으로 완료")
    else:
        logger.warning("⚠️ 일부 단계에서 실패 발생")


if __name__ == "__main__":
    main()
