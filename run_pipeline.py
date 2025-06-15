import logging
import subprocess
import sys
import os
from datetime import datetime

from src.db_handler import update_db_status

from src.db_handler import update_db_status

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# ---------------------- 실행할 스크립트 순서 정의 ----------------------
PIPELINE_SEQUENCE = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py"
]

# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(script):
    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logging.error(f"❌ 파일이 존재하지 않습니다: {full_path}")
        return False

    logging.info(f"🚀 실행 중: {script}")
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"❌ 실패: {script}\n{result.stderr}")
        return False
    else:
        logging.info(f"✅ 완료: {script}")
        if result.stdout.strip():
            print(result.stdout)
        return True

# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline():
    logging.info(f"🧩 파이프라인 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    update_db_status("Pipeline Start", "In Progress")
    all_passed = True

    for script in PIPELINE_SEQUENCE:
        success = run_script(script)
        update_db_status(script, "Success" if success else "Failed")
        if not success:
            all_passed = False
            # 실패해도 계속 실행할 것인지 중단할 것인지 선택 가능
            # break

    logging.info("🎯 파이프라인 전체 완료")
    if all_passed:
        logging.info("✅ 모든 단계 성공적으로 완료")
        update_db_status("Pipeline End", "Completed")
    else:
        logging.warning("⚠️ 일부 단계에서 실패 발생")
        update_db_status("Pipeline End", "Failed")

# ---------------------- 진입점 ----------------------
if __name__ == "__main__":
    run_pipeline()
