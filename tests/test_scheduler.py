"""Tests for the scheduler module."""

from unittest.mock import patch
import schedule

import scheduler


def test_job_triggers_pipeline_and_prints(capsys):
    """Ensure job prints the trigger message and calls the pipeline."""
    with patch('scheduler.run_pipeline') as run_mock:
        scheduler.job()
        captured = capsys.readouterr()
        assert "Content Pipeline Triggered" in captured.out
        run_mock.assert_called_once()


def test_setup_scheduler_adds_daily_job():
    """Verify that a job is scheduled for 10:00 every day."""
    schedule.clear()
    scheduler.setup_scheduler()
    jobs = schedule.get_jobs()
    assert len(jobs) == 1
    job = jobs[0]
    assert job.at_time.hour == 10
    assert job.at_time.minute == 0
    schedule.clear()
