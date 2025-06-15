import logging
import subprocess
import sys
import os
from datetime import datetime
import argparse

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# ---------------------- 실행할 스크립트 순서 정의 ----------------------
PIPELINE_SEQUENCE: list[str] = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py"
]

# ---------------------- CLI 파서 ----------------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only", help="comma-sep step list")
    p.add_argument("--skip", help="comma-sep step list")
    return p.parse_args()

# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(script: str, dry_run: bool = False) -> bool:
    if dry_run:
        print(script)
        return True
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
def run_pipeline(steps: list[str], dry_run: bool = False) -> None:
    logging.info(
        f"🧩 파이프라인 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    all_passed = True

    for script in steps:
        success = run_script(script, dry_run=dry_run)
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
    args = parse_args()
    steps = PIPELINE_SEQUENCE[:]
    if args.only:
        whitelist = set(x.strip() for x in args.only.split(","))
        steps = [s for s in steps if s in whitelist]
    if args.skip:
        blacklist = set(x.strip() for x in args.skip.split(","))
        steps = [s for s in steps if s not in blacklist]
    run_pipeline(steps, dry_run=args.dry_run)
