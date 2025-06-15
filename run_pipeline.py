import logging
import subprocess
import sys
import os
from datetime import datetime

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# ---------------------- 실행할 스크립트 순서 정의 ----------------------
PIPELINE_SEQUENCE = [
    "hook_generator.py",
    "notion_hook_uploader.py",
    "retry_failed_uploads.py",
    "retry_dashboard_notifier.py",
]

# ---------------------- 스크립트 실행 함수 ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(script: str) -> bool:
    """Run a script located in the repository root."""
    full_path = os.path.join(BASE_DIR, script)
    if not os.path.exists(full_path):
        logging.error("❌ 파일이 존재하지 않습니다: %s", full_path)
        return False

    logging.info("🚀 실행 중: %s", script)
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error("❌ 실패: %s\n%s", script, result.stderr)
        return False
    else:
        logging.info("✅ 완료: %s", script)
        if result.stdout.strip():
            print(result.stdout)
        return True

# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline():
    logging.info(f"🧩 파이프라인 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_passed = True

    for script in PIPELINE_SEQUENCE:
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
    run_pipeline()
