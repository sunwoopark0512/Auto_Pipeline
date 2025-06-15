"""Simple scheduler using schedule library."""

import schedule
import time
from typing import Callable


def schedule_job(job: Callable, interval: int = 1) -> None:
    """Schedule a job every `interval` minutes."""
    schedule.every(interval).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
