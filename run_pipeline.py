"""v-Infinity 콘텐츠 자동화 파이프라인 런너.

지정된 모듈들을 순차적으로 실행하고, 실패 정보를 최종 알림 스텝에 전달한다.
"""

from __future__ import annotations

import importlib.util
import logging
import sys
from pathlib import Path
from types import ModuleType

PIPELINE_ORDER: list[str] = [
    "hook_generator",
    "keyword_auto_pipeline",
    "notion_hook_uploader",
    "retry_dashboard_notifier",  # 항상 마지막
]

BASE_DIR = Path(__file__).resolve().parent
LOGGER = logging.getLogger(__name__)


def _setup_logging() -> None:
    """Configure structured logging for ingestion."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}'
    )
    handler.setFormatter(formatter)
    LOGGER.setLevel(logging.INFO)
    LOGGER.addHandler(handler)


def _dynamic_import(module_name: str) -> ModuleType:
    """Import a module from ``BASE_DIR`` by name.

    Args:
        module_name: File stem without ``.py``.

    Returns:
        Module object.

    Raises:
        ValueError: If the module file does not exist.
    """
    module_path = BASE_DIR / f"{module_name}.py"
    if not module_path.exists():
        raise ValueError(f"Unknown step: {module_name}")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


def _run_step(module: ModuleType) -> None:
    """Run a pipeline step that exposes ``main()``."""
    if not hasattr(module, "main"):
        raise AttributeError(f"{module.__name__} has no main()")
    LOGGER.info("▶︎ step_start %s", module.__name__)
    module.main()  # type: ignore[attr-defined]
    LOGGER.info("✔︎ step_done %s", module.__name__)


def main() -> None:
    """Execute the pipeline in ``PIPELINE_ORDER`` with graceful teardown."""
    _setup_logging()
    failures: list[str] = []

    for name in PIPELINE_ORDER[:-1]:
        try:
            _run_step(_dynamic_import(name))
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception("step_failed %s", name)
            failures.append(name)

    notifier = _dynamic_import(PIPELINE_ORDER[-1])
    notifier.main(failures=failures)  # type: ignore[arg-type]


if __name__ == "__main__":
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        LOGGER.exception("pipeline_crashed")
        sys.exit(1)
