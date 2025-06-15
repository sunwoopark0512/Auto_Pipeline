"""Simple scheduler to trigger the content pipeline."""

import time
import schedule

from run_pipeline import run_pipeline


def job() -> None:
    """Trigger the content pipeline."""
    print("🚀 Content Pipeline Triggered")
    run_pipeline()


def setup_scheduler() -> None:
    """Configure the daily schedule."""
    schedule.every().day.at("10:00").do(job)


def start_scheduler() -> None:
    """Start the scheduler loop."""
    setup_scheduler()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
