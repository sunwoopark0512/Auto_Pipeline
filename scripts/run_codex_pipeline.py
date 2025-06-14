import os
import subprocess
import sys
import logging
import yaml
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

with open(os.path.join('config', 'pipeline.yaml')) as f:
    PIPELINE_SEQUENCE = yaml.safe_load(f)['pipeline_sequence']

def run_script(script: str) -> bool:
    full_path = os.path.join(BASE_DIR, script)
    if not os.path.exists(full_path):
        logging.error(f"❌ 파일이 존재하지 않습니다: {full_path}")
        return False

    logging.info(f"🚀 실행 중: {script}")
    result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"❌ 실패: {script}\n{result.stderr}")
        return False
    logging.info(f"✅ 완료: {script}")
    if result.stdout.strip():
        print(result.stdout)
    return True

def run_pipeline() -> None:
    logging.info(f"🧩 파이프라인 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_passed = True
    for script in PIPELINE_SEQUENCE:
        success = run_script(script)
        if not success:
            all_passed = False
    logging.info("🎯 파이프라인 전체 완료")
    if all_passed:
        logging.info("✅ 모든 단계 성공적으로 완료")
    else:
        logging.warning("⚠️ 일부 단계에서 실패 발생")

if __name__ == '__main__':
    run_pipeline()
