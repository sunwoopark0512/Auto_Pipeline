"""Pipeline runner script for orchestrating all steps."""

import argparse
import logging
import os
import subprocess
import sys
from datetime import datetime

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

# ---------------------- 실행할 스크립트 순서 정의 ----------------------
PIPELINE_SEQUENCE = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py",
]


# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(script: str) -> bool:
    """Run a pipeline step script and return success status."""

    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logging.error("❌ 파일이 존재하지 않습니다: %s", full_path)
        return False

    logging.info("🚀 실행 중: %s", script)
    result = subprocess.run(
        [sys.executable, full_path], capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        logging.error("❌ 실패: %s\n%s", script, result.stderr)
        return False

    logging.info("✅ 완료: %s", script)
    if result.stdout.strip():
        print(result.stdout)
    return True


# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline(dry_run: bool = False) -> None:
    """Run the full pipeline or print steps when dry running."""

    logging.info("🧩 파이프라인 시작: %s", datetime.now().strftime("%Y-%m-%d %H:%M"))
    all_passed = True

    for script in PIPELINE_SEQUENCE:
        if dry_run:
            logging.info("[dry-run] would run: %s", script)
            continue

        success = run_script(script)
        if not success:
            all_passed = False
            # 실패해도 계속 실행할 것인지 중단할 것인지 선택 가능
            # break

    logging.info("🎯 파이프라인 전체 완료")
    if all_passed:
        logging.info("✅ 모든 단계 성공적으로 완료")
    else:
        logging.warning("⚠️ 일부 단계에서 실패 발생")


# ---------------------- 진입점 ----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List scripts without executing",
    )
    args = parser.parse_args()

    run_pipeline(dry_run=args.dry_run)
