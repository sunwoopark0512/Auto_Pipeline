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
    "retry_failed_uploads.py",
    "retry_dashboard_notifier.py"
]

# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(script: str) -> bool:
    """Execute a script found either in the project root or under ``scripts/``."""
    candidate_paths = [
        os.path.join("scripts", script),
        script,
    ]

    for path in candidate_paths:
        if os.path.exists(path):
            logging.info(f"🚀 실행 중: {script}")
            result = subprocess.run([sys.executable, path], capture_output=True, text=True)

            if result.returncode != 0:
                logging.error(f"❌ 실패: {script}\n{result.stderr}")
                return False

            logging.info(f"✅ 완료: {script}")
            if result.stdout.strip():
                print(result.stdout)
            return True

    logging.error(f"❌ 파일이 존재하지 않습니다: {script}")
    return False

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
