"""v-Infinity 콘텐츠 자동화 파이프라인 런너.

지정된 모듈들을 순차적으로 실행하고, 실패 정보를 최종 알림 스텝에 전달한다.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import logging
import os
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
_LOADED_PATHS: dict[str, Path] = {}


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
    """Import ``module_name`` from the root or ``scripts`` folder.

    Raises a ``ValueError`` if the module is not found or has already been
    imported under a different name.
    """

    module_path = BASE_DIR / f"{module_name}.py"
    if not module_path.exists():
        alt = BASE_DIR / "scripts" / f"{module_name}.py"
        if alt.exists():
            module_path = alt
        else:
            LOGGER.error(
                "step_import_fail %s", module_name, extra={"step": module_name, "event": "import_fail"}
            )
            raise ValueError(f"Unknown step: {module_name}")

    real_path = module_path.resolve()
    for mod, seen in _LOADED_PATHS.items():
        try:
            if real_path.samefile(seen) and mod != module_name:
                raise ImportError(
                    f"Duplicate module path detected: {module_name} conflicts with {mod}"
                )
        except FileNotFoundError:
            if real_path == seen and mod != module_name:
                raise ImportError(
                    f"Duplicate module path detected: {module_name} conflicts with {mod}"
                )
    _LOADED_PATHS[module_name] = real_path

    spec = importlib.util.spec_from_file_location(module_name, real_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


def _import_and_run(step: str, dry_run: bool) -> None:
    """Import ``step`` and execute its ``main`` function.

    Parameters
    ----------
    step:
        Module name without ``.py``.
    dry_run:
        If ``True``, skip actual execution.
    """

    try:
        module = _dynamic_import(step)
        _run_step(module, dry_run=dry_run)
    except Exception as ex:  # pylint: disable=broad-except
        LOGGER.exception("\u274c Step failed", extra={"step": step})
        raise ex


def _run_step(module: ModuleType, dry_run: bool = False) -> None:
    """Run a pipeline step that exposes ``main()``.

    Parameters
    ----------
    module:
        Imported module exposing ``main``.
    dry_run:
        If ``True``, the step will be skipped but reported as started and done.
    """
    if not hasattr(module, "main"):
        raise AttributeError(f"{module.__name__} has no main()")
    LOGGER.info("step_start %s", module.__name__, extra={"step": module.__name__, "event": "step_start"})
    if not dry_run:
        module.main()  # type: ignore[attr-defined]
    LOGGER.info("step_done %s", module.__name__, extra={"step": module.__name__, "event": "step_done"})
    sys.modules.pop(module.__name__, None)


def main(argv: list[str] | None = None) -> None:
    """Execute the pipeline in ``PIPELINE_ORDER`` with graceful teardown."""
    parser = argparse.ArgumentParser(description="Execute the content pipeline")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Import steps without executing them",
    )
    args = parser.parse_args(argv if argv is not None else [])

    _setup_logging()
    failures: list[str] = []

    if args.dry_run:
        os.environ["DRY_RUN"] = "1"
    else:
        os.environ.pop("DRY_RUN", None)

    for name in PIPELINE_ORDER[:-1]:
        try:
            _import_and_run(name, dry_run=args.dry_run)
        except Exception:  # pylint: disable=broad-except
            failures.append(name)

    notifier = _dynamic_import(PIPELINE_ORDER[-1])
    notifier.main(failures=failures)  # type: ignore[arg-type]
    if failures and not args.dry_run:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # pylint: disable=broad-except
        LOGGER.exception("pipeline_crashed", extra={"event": "pipeline_crashed"})
        sys.exit(1)
