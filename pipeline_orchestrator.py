"""Utility to orchestrate the full Notion hook pipeline."""

from datetime import datetime
from pathlib import Path
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Scripts to run for the main pipeline
PIPELINE_SEQUENCE = [
    'keyword_auto_pipeline.py',
    'hook_generator.py',
    'notion_hook_uploader.py'
]

# Scripts to run regardless of previous failures
FALLBACK_SEQUENCE = [
    'retry_failed_uploads.py',
    'retry_dashboard_notifier.py'
]

def run_script(script: str) -> bool:
    """Run a Python script and return True if it succeeds."""
    path = Path(script)
    if not path.exists():
        logging.error("❌ 파일이 존재하지 않습니다: %s", path)
        return False

    logging.info("🚀 실행 중: %s", path)
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        logging.error("❌ 실패: %s\n%s", path, exc.stderr)
        return False

    if result.stdout.strip():
        print(result.stdout)
    logging.info("✅ 완료: %s", path)
    return True

def run_pipeline() -> None:
    """Run full pipeline with fallback on failure."""
    logging.info("🧩 파이프라인 시작: %s", datetime.now().strftime('%Y-%m-%d %H:%M'))
    failures = []

    for script in PIPELINE_SEQUENCE:
        if not run_script(script):
            failures.append(script)

    # Always run fallback scripts
    for script in FALLBACK_SEQUENCE:
        run_script(script)

    if failures:
        logging.warning("⚠️ 실패한 단계: %s", ', '.join(failures))
    else:
        logging.info("✅ 모든 단계 성공적으로 완료")

if __name__ == '__main__':
    run_pipeline()
