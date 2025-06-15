# -------------------- filename: super_scheduler.py ------------------------

import time
import logging
from datetime import datetime

import orchestrator
import notion_sync
import strategy_optimizer
import webhook_receiver

# 스케줄 간격 (초 단위, 실서비스에선 분단위로 조정 가능)
CYCLE_TIME_SEC = 60 * 60  # 1시간 간격
NOTION_SYNC_CYCLE = 3  # 매 3주기마다 실행
STRATEGY_OPTIMIZE_CYCLE = 24  # 매 24주기마다 실행

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_scheduler():
    cycle_count = 0
    logging.info("=== v-Infinity SuperScheduler 시작 ===")

    while True:
        cycle_count += 1
        start = datetime.now()

        logging.info(f"===== 🔄 주기 {cycle_count} 시작 =====")

        try:
            # 메인 파이프라인
            failures = orchestrator.run_full_pipeline()
            if failures:
                logging.error(f"Orchestrator 실패 단계: {failures}")

            # Notion Sync 매 N주기마다 실행
            if cycle_count % NOTION_SYNC_CYCLE == 0:
                logging.info("📊 Notion Sync 실행")
                notion_sync.sync("content", limit=50)

            # Strategy Optimizer 매 N주기마다 실행
            if cycle_count % STRATEGY_OPTIMIZE_CYCLE == 0:
                logging.info("🧠 Strategy Optimizer 실행")
                strategy_optimizer.process("content", days=30)

            # Webhook Receiver 상태 로그
            logging.info("🌐 Webhook Receiver 정상 대기 중")

        except Exception as e:
            logging.error(f"❌ Scheduler 주기 오류: {e}")

        duration = (datetime.now() - start).total_seconds()
        logging.info(f"⏱️ 주기 소요시간: {duration:.1f}초 / 대기 {CYCLE_TIME_SEC}s")

        time.sleep(CYCLE_TIME_SEC)


if __name__ == "__main__":
    run_scheduler()
