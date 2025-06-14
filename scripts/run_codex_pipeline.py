#!/usr/bin/env python3
"""Run the full Codex pipeline."""
import logging
import subprocess
import sys
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

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
        logging.error(f"\u274c 파일이 존재하지 않습니다: {full_path}")
        return False
    logging.info(f"\ud83d\ude80 실행 중: {script}")
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"\u274c 실패: {script}\n{result.stderr}")
        return False
    logging.info(f"\u2705 완료: {script}")
    if result.stdout.strip():
        print(result.stdout)
    return True

def run_pipeline() -> None:
    logging.info(f"\ud83e\uddf0 파이프라인 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_passed = True
    for script in PIPELINE_SEQUENCE:
        if not run_script(script):
            all_passed = False
    logging.info("\ud83c\udf3f 파이프라인 전체 완료")
    if all_passed:
        logging.info("\u2705 모든 단계 성공적으로 완료")
    else:
        logging.warning("\u26a0\ufe0f 일부 단계에서 실패 발생")

if __name__ == "__main__":
    run_pipeline()
