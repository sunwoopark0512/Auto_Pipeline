"""
Run health-checks for every pipeline step listed in PIPELINE_ORDER
and publish a Slack summary (+ exit code).

CLI:
    python qa_tester.py --config pipeline_config.py
"""

from __future__ import annotations

import importlib
import os
import sys
import traceback
from argparse import ArgumentParser
from datetime import datetime, timezone
from typing import List

from slack_sdk.webhook import WebhookClient


# -------------------- 환경 변수 -------------------- #
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SUMMARY_CHANNEL = WebhookClient(SLACK_WEBHOOK_URL) if SLACK_WEBHOOK_URL else None


class StepResult:
    """간단한 결과 DTO."""

    def __init__(self, name: str):
        self.name = name
        self.success = False
        self.error: str | None = None
        self.traceback: str | None = None


def _load_pipeline_order(cfg_module):
    if not hasattr(cfg_module, "PIPELINE_ORDER") or not isinstance(
        cfg_module.PIPELINE_ORDER, list
    ):
        raise AttributeError("Config must define list `PIPELINE_ORDER`.")
    return cfg_module.PIPELINE_ORDER


def _run_step(step: str) -> StepResult:
    res = StepResult(step)
    try:
        mod = importlib.import_module(step)
        if hasattr(mod, "main"):
            mod.main()
        res.success = True
    except Exception as exc:  # pylint: disable=broad-except
        res.error = str(exc)
        res.traceback = traceback.format_exc(limit=5)
    return res


def _notify_slack(results: List[StepResult]):
    if SUMMARY_CHANNEL is None:
        return
    ok = sum(r.success for r in results)
    fail = len(results) - ok
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    color = "#2ecc71" if fail == 0 else "#e74c3c"
    text_lines = [f"*QA Report {ts}* – ✅ {ok} | ❌ {fail}"]
    for r in results:
        emoji = "✅" if r.success else "❌"
        text_lines.append(f"{emoji} `{r.name}`")
        if r.error:
            text_lines.append(f"> {r.error}")
    SUMMARY_CHANNEL.send(
        attachments=[{"color": color, "text": "\n".join(text_lines)}]
    )


def run_health_checks(config_path: str) -> int:
    """0 = all good, 1 = any failure."""
    cfg = importlib.import_module(config_path.replace("/", ".").rstrip(".py"))
    order = _load_pipeline_order(cfg)
    results = [_run_step(step) for step in order]
    _notify_slack(results)
    for r in results:
        status = "OK" if r.success else "FAIL"
        print(f"[{status}] {r.name}")
        if r.traceback:
            print(r.traceback)
    return 0 if all(r.success for r in results) else 1


def _cli():
    parser = ArgumentParser(description="Pipeline QA health-checker")
    parser.add_argument("--config", required=True, help="Path to pipeline_config.py")
    args = parser.parse_args()
    sys.exit(run_health_checks(args.config))


if __name__ == "__main__":
    _cli()
