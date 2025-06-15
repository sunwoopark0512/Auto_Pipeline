import logging
import subprocess
import sys
import os
from datetime import datetime
from importlib import util
import importlib

from scripts.tracing import start_span

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

_loaded_hashes = set()

def _import_and_run(module_name: str):
    """Import a module by name and run its main() function once."""
    spec = util.find_spec(module_name)
    if not spec or not spec.origin:
        raise ImportError(f"Cannot find module {module_name}")
    with open(spec.origin, "r", encoding="utf-8") as f:
        src_hash = hash(f.read())
    if src_hash in _loaded_hashes:
        raise ImportError(f"Duplicate module import: {module_name}")
    _loaded_hashes.add(src_hash)

    module = importlib.import_module(module_name)
    if hasattr(module, "main"):
        module.main()
    return module

# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(script):
    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logging.error("❌ 파일이 존재하지 않습니다: %s", full_path, extra={"step": script})
        return False

    logging.info("🚀 실행 중: %s", script, extra={"step": script})
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error("❌ 실패: %s\n%s", script, result.stderr, extra={"step": script})
        return False
    else:
        logging.info("✅ 완료: %s", script, extra={"step": script})
        if result.stdout.strip():
            print(result.stdout)
        return True

# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline():
    logging.info("🧩 파이프라인 시작: %s", datetime.now().strftime('%Y-%m-%d %H:%M'), extra={"step": "start"})
    all_passed = True

    for script in PIPELINE_SEQUENCE:
        step_name = script.replace('.py', '')
        with start_span(step_name):
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
