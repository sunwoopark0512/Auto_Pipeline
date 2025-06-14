"""Execute pipeline steps sequentially."""

import logging
import os
import subprocess
import sys
from datetime import datetime

from scripts.tracing import span

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
def run_script(script):
    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logging.error("\u274c 파일이 존재하지 않습니다: %s", full_path)
        return False

    logging.info("\U0001f680 실행 중: %s", script)
    result = subprocess.run(
        [sys.executable, full_path], capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        logging.error("\u274c 실패: %s\n%s", script, result.stderr)
        return False
    else:
        logging.info("\u2705 완료: %s", script)
        if result.stdout.strip():
            print(result.stdout)
        return True


# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline():
    logging.info("\U0001f9e9 파이프라인 시작: %s", datetime.now().strftime("%Y-%m-%d %H:%M"))
    all_passed = True

    for script in PIPELINE_SEQUENCE:
        with span("pipeline.step", step=script):
            success = run_script(script)
        if not success:
            all_passed = False
            # 실패해도 계속 실행할 것인지 중단할 것인지 선택 가능
            # break

    logging.info("\U0001f3af 파이프라인 전체 완료")
    if all_passed:
        logging.info("\u2705 모든 단계 성공적으로 완료")
    else:
        logging.warning("\u26a0\ufe0f 일부 단계에서 실패 발생")


# ---------------------- 진입점 ----------------------
if __name__ == "__main__":
    run_pipeline()
