"""
Dynamic pipeline runner with structured JSON logging, fail-fast check,
and graceful teardown.

CLI:
    python run_pipeline.py --config pipeline_config
"""

from __future__ import annotations

import importlib
import logging
import sys
from argparse import ArgumentParser
from types import ModuleType
from typing import List, Optional

from pythonjsonlogger import jsonlogger

_LOG = logging.getLogger("pipeline")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
)
_LOG.addHandler(handler)
_LOG.setLevel(logging.INFO)


def _load_config(path: str) -> ModuleType:
    if path.endswith(".py"):
        path = path[:-3]
    return importlib.import_module(path.replace("/", ".").rstrip(".py"))


def _validate_steps(cfg: ModuleType):
    if not hasattr(cfg, "PIPELINE_ORDER") or not isinstance(cfg.PIPELINE_ORDER, list):
        raise AttributeError("Config must define list `PIPELINE_ORDER`.")
    for step in cfg.PIPELINE_ORDER:
        try:
            importlib.import_module(step)
        except ModuleNotFoundError as exc:
            raise ValueError(f"Unknown step: {step}") from exc


def _run_step(step: str) -> Optional[str]:
    try:
        mod = importlib.import_module(step)
        _LOG.info("step_start", extra={"step": step})
        if hasattr(mod, "main"):
            mod.main()
        else:
            _LOG.warning("step_no_main", extra={"step": step})
        _LOG.info("step_success", extra={"step": step})
        return None
    except Exception as exc:  # pylint: disable=broad-except
        _LOG.error("step_fail", extra={"step": step, "error": str(exc)})
        return step


def _run_notifier(cfg: ModuleType, failures: List[str]):
    step = getattr(cfg, "NOTIFIER_STEP", None)
    if not step:
        return
    try:
        mod = importlib.import_module(step)
        if hasattr(mod, "main"):
            mod.main(failures)
            _LOG.info("notifier_success", extra={"step": step, "failures": failures})
    except Exception as exc:  # pylint: disable=broad-except
        _LOG.error("notifier_fail", extra={"step": step, "error": str(exc)})


def run_pipeline(cfg_path: str) -> int:
    cfg = _load_config(cfg_path)
    _validate_steps(cfg)

    failures: List[str] = []
    for step in cfg.PIPELINE_ORDER:
        err = _run_step(step)
        if err:
            failures.append(err)

    _run_notifier(cfg, failures)
    return 0 if not failures else 1


def _cli():
    ap = ArgumentParser(description="Run content-automation pipeline")
    ap.add_argument("--config", default="pipeline_config", help="Config module path")
    args = ap.parse_args()
    sys.exit(run_pipeline(args.config))


if __name__ == "__main__":  # guard → 임포트 시 부작용 방지
    _cli()
