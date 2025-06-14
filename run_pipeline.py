"""Pipeline runner script for orchestrating all steps."""

import argparse
import importlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, List, Set

from scripts.logger import setup_logger

# ---------------------- 로깅 설정 ----------------------
logger = setup_logger(__name__)  # JSON logger

# ---------------------- 실행할 스크립트 순서 정의 ----------------------
PIPELINE_SEQUENCE = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py",
]

LOADED_STEPS: Set[str] = set()  # 중복 스크립트 로드 방지


# ---------------------- 유틸: 동적 임포트 ----------------------
def _dynamic_import(module_name: str) -> Any:
    """모듈을 동적 임포트한다.

    1) 루트 → 2) scripts/ 순서로 시도하며,
    두 위치 모두 존재하면 중복 오류를 기록한다.
    """
    root_path = Path(f"{module_name}")
    scripts_path = Path("scripts") / module_name

    duplicates = [p for p in (root_path, scripts_path) if p.exists()]
    if len(duplicates) > 1:
        logger.error(
            "duplicate_module",
            extra={"step": module_name, "paths": [str(p) for p in duplicates]},
        )
        raise ImportError(f"Duplicate module found: {duplicates}")

    try:
        return importlib.import_module(module_name.rstrip(".py"))
    except ImportError:
        return importlib.import_module(f"scripts.{module_name.rstrip('.py')}")


# ---------------------- 스크립트 실행 함수 ----------------------
def run_script(script: str) -> bool:
    """Import and execute a pipeline step."""

    if script in LOADED_STEPS:
        logger.warning("step_already_loaded", extra={"step": script})
        return True

    try:
        module = _dynamic_import(script)
        LOADED_STEPS.add(script)
        if hasattr(module, "main"):
            module.main()
        else:
            logger.error("missing_main", extra={"step": script})
            return False
    except Exception as err:  # pylint: disable=broad-except
        logger.error(
            "step_failed",
            extra={"step": script, "error": str(err)},
        )
        return False

    logger.info("step_completed", extra={"step": script})
    return True


# ---------------------- 전체 파이프라인 실행 ----------------------
def run_pipeline(dry_run: bool = False, only: List[str] | None = None) -> None:
    """Run the full pipeline or selected steps."""

    logger.info(
        "pipeline_start", extra={"time": datetime.now().strftime("%Y-%m-%d %H:%M")}
    )
    failed_steps: List[str] = []
    targets = only or PIPELINE_SEQUENCE

    for script in targets:
        if dry_run:
            logger.info("dry_run_step", extra={"step": script})
            continue

        success = run_script(script)
        if not success:
            failed_steps.append(script)
            # 실패해도 계속 실행할 것인지 중단할 것인지 선택 가능
            # break

    logger.info("pipeline_end")
    if failed_steps:
        logger.warning("⚠️ 일부 단계 실패: %s", failed_steps)
        sys.exit(1)
    logger.info("✅ 모든 단계 성공적으로 완료")


# ---------------------- 진입점 ----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run pipeline")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List scripts without executing",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        help="Run only specified scripts",
    )
    args = parser.parse_args()

    run_pipeline(dry_run=args.dry_run, only=args.only)
