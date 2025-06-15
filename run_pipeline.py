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
PIPELINE_ORDER = [
    "hook_generator",
    "notion_hook_uploader",
    "retry_failed_uploads",
    "retry_dashboard_notifier",
]

# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(module_name, loaded=None):
    script_path = f"{module_name}.py"
    if not os.path.exists(script_path):
        logging.error(f"❌ 파일이 존재하지 않습니다: {script_path}")
        return False

    if loaded is not None:
        if module_name in loaded:
            raise ImportError(f"중복 모듈 로드 시도: {module_name}")
        loaded.add(module_name)

    logging.info(f"🚀 실행 중: {script_path}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"❌ 실패: {module_name}\n{result.stderr}")
        return False
    else:
        logging.info(f"✅ 완료: {module_name}")
        if result.stdout.strip():
            print(result.stdout)
        return True

# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline():
    logging.info(f"🧩 파이프라인 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_passed = True
    loaded = set()

    for script in PIPELINE_ORDER:
        success = run_script(script, loaded)
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
