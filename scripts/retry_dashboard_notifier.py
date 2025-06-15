"""Wrapper to update KPI dashboards using :mod:`retry_dashboard_notifier`."""

import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # pylint: disable=wrong-import-position

from retry_dashboard_notifier import get_retry_stats, push_kpi_to_notion  # type: ignore

if __name__ == "__main__":
    kpi = get_retry_stats()
    if kpi:
        logging.info("📈 KPI 요약: %s", kpi)
        push_kpi_to_notion(kpi)
