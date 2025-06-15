#!/usr/bin/env python3
"""QA automation script for pipeline validation and optional Retool reporting."""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
from typing import List, Dict, Any

try:
    import requests
except ImportError as exc:  # pragma: no cover - should be preinstalled
    raise SystemExit("The 'requests' package is required to run this script") from exc


PIPELINE_SEQUENCE: List[str] = [
    "hook_generator.py",
    "parse_failed_gpt.py",
    "retry_failed_uploads.py",
    "notify_retry_result.py",
    "retry_dashboard_notifier.py",
]


def run_script(script: str) -> Dict[str, Any]:
    """Run a script and capture its result."""
    full_path = os.path.join("scripts", script)
    if not os.path.exists(full_path):
        logging.warning("파일이 존재하지 않습니다: %s", full_path)
        return {"script": script, "status": "missing"}

    logging.info("실행: %s", script)
    result = subprocess.run(
        [sys.executable, full_path],
        capture_output=True,
        text=True,
        check=False,
    )
    status = "success" if result.returncode == 0 else "failed"
    return {
        "script": script,
        "status": status,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def run_pipeline(sequence: List[str]) -> List[Dict[str, Any]]:
    """Execute the pipeline sequence and collect results."""
    results = []
    for script in sequence:
        results.append(run_script(script))
    return results


def send_to_retool(webhook: str, results: List[Dict[str, Any]]) -> bool:
    """Send results to a Retool webhook."""
    try:
        response = requests.post(webhook, json={"results": results}, timeout=10)
        response.raise_for_status()
        return True
    except Exception as exc:  # pragma: no cover - network errors
        logging.error("Retool 전송 실패: %s", exc)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI QA 자동화 스크립트")
    parser.add_argument(
        "--webhook",
        help="Retool webhook URL (또는 환경 변수 RETOOL_WEBHOOK_URL 사용)",
    )
    args = parser.parse_args()

    logging.info("QA 테스트 시작")
    results = run_pipeline(PIPELINE_SEQUENCE)
    logging.info("QA 테스트 완료")

    webhook = args.webhook or os.getenv("RETOOL_WEBHOOK_URL")
    if webhook:
        if send_to_retool(webhook, results):
            logging.info("Retool로 결과 전송 성공")
        else:
            logging.error("Retool로 결과 전송 실패")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
    main()
