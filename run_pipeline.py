import logging
import subprocess
import sys
import os
import time
from datetime import datetime
from prometheus_client import start_http_server, Summary, Counter

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

# ---------------------- 외부 서비스 초기화 ----------------------
try:
    import sentry_sdk
    sentry_sdk.init(os.getenv("SENTRY_DSN", ""))
except Exception as e:
    logging.warning(f"Sentry init failed: {e}")
    sentry_sdk = None

try:
    import newrelic.agent
    newrelic.agent.initialize(os.getenv("NEW_RELIC_CONFIG_FILE", ""))
except Exception as e:
    logging.warning(f"New Relic init failed: {e}")

# ---------------------- Prometheus 메트릭 설정 ----------------------
METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))
start_http_server(METRICS_PORT)
SCRIPT_DURATION = Summary('script_execution_seconds', 'Time spent executing script', ['script'])
SCRIPT_SUCCESS = Counter('script_success_total', 'Script success count', ['script'])
SCRIPT_FAILURE = Counter('script_failure_total', 'Script failure count', ['script'])

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
        SCRIPT_FAILURE.labels(script=script).inc()
        if sentry_sdk:
            sentry_sdk.capture_exception(FileNotFoundError(full_path))
        return False

    logging.info(f"🚀 실행 중: {script}")
    start_time = time.time()
    try:
        result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)
    except Exception as e:
        SCRIPT_FAILURE.labels(script=script).inc()
        if sentry_sdk:
            sentry_sdk.capture_exception(e)
        logging.error(f"❌ 실행 오류: {script} - {e}")
        return False
    duration = time.time() - start_time
    SCRIPT_DURATION.labels(script=script).observe(duration)

    if result.returncode != 0:
        logging.error(f"❌ 실패: {script}\n{result.stderr}")
        SCRIPT_FAILURE.labels(script=script).inc()
        if sentry_sdk:
            sentry_sdk.capture_exception(Exception(result.stderr))
        return False
    else:
        logging.info(f"✅ 완료: {script}")
        SCRIPT_SUCCESS.labels(script=script).inc()
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
    try:
        run_pipeline()
    except Exception as e:
        if sentry_sdk:
            sentry_sdk.capture_exception(e)
        raise
