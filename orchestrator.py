import logging
import os
import signal
import time
from datetime import datetime
from typing import List

import content_formatter
import snippet_generator
import ab_variant_manager
import auto_rewriter
import qa_tester
import podcast_creator
import graphic_generator
import hook_uploader
import osmu_analytics

TABLE_NAME = "content"
LIMIT = 5
DAYS_LOOKBACK = 7

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

stop_requested = False

def handle_sigterm(signum, frame):
    global stop_requested
    logging.info("🛑 SIGTERM received. Will exit after current step.")
    stop_requested = True

signal.signal(signal.SIGTERM, handle_sigterm)

def step(name: str, func, *args, **kwargs) -> bool:
    if stop_requested:
        logging.info(f"⏹️ {name} skipped due to stop request")
        return False
    started = time.time()
    try:
        logging.info(f"🚀 {name} 시작")
        func(*args, **kwargs)
        elapsed = time.time() - started
        logging.info(f"✅ {name} 완료 (⏱️ {elapsed:.1f}초)")
        return True
    except Exception as e:
        elapsed = time.time() - started
        logging.error(f"❌ {name} 실패: {e} (⏱️ {elapsed:.1f}초)")
        return False

def run_full_pipeline() -> List[str]:
    failures = []

    if not step("A/B Variants 생성", ab_variant_manager.process_batch, TABLE_NAME, LIMIT, 3, 2):
        failures.append("ab_variant_manager")
        if stop_requested:
            return failures

    if not step("Rewriter 실행", auto_rewriter.rewrite_batch, TABLE_NAME, 0.3):
        failures.append("auto_rewriter")
        if stop_requested:
            return failures

    if not step("QA Health Check", qa_tester.run_health_checks, "pipeline_config"):
        failures.append("qa_tester")
        if stop_requested:
            return failures

    if not step("Podcast 생성", podcast_creator.process_batch, TABLE_NAME, LIMIT):
        failures.append("podcast_creator")
        if stop_requested:
            return failures

    if not step("Graphic 생성", graphic_generator.process_batch, TABLE_NAME, LIMIT):
        failures.append("graphic_generator")
        if stop_requested:
            return failures

    if not step("Uploader 실행", hook_uploader.publish_batch, TABLE_NAME, LIMIT):
        failures.append("hook_uploader")
        if stop_requested:
            return failures

    if not step("OSMU Analytics", osmu_analytics.process, TABLE_NAME, DAYS_LOOKBACK, 50):
        failures.append("osmu_analytics")
        if stop_requested:
            return failures

    return failures

if __name__ == "__main__":
    logging.info("===== v-Infinity Full Pipeline 시작 =====")
    started_at = datetime.now()

    failures = run_full_pipeline()

    elapsed = (datetime.now() - started_at).total_seconds()
    if stop_requested:
        logging.info("🛑 파이프라인이 중단되었습니다")
    elif failures:
        logging.error(f"전체 실패 단계: {failures}")
    else:
        logging.info("🎉 전체 파이프라인 성공 완료")

    logging.info(f"⏱️ 총 소요 시간: {elapsed:.1f}초")
