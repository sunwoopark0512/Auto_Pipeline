"""Utilities for retry logic."""

from tenacity import retry, wait_exponential_jitter, stop_after_attempt


def gpt_retry():
    """Return a tenacity.retry decorator tuned for GPT calls."""
    return retry(
        reraise=True,
        wait=wait_exponential_jitter(initial=1, max=20),
        stop=stop_after_attempt(6),
    )
