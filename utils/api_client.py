"""HTTP client with timeout and retry."""
from __future__ import annotations

import logging
from typing import Optional

import requests


DEFAULT_TIMEOUT = 10


def request_with_retry(url: str, *, method: str = "GET", retries: int = 3, timeout: int = DEFAULT_TIMEOUT, **kwargs) -> Optional[requests.Response]:
    for attempt in range(1, retries + 1):
        try:
            resp = requests.request(method, url, timeout=timeout, **kwargs)
            if resp.status_code == 429:
                logging.warning("HTTP 429 received, retrying %s/%s", attempt, retries)
                continue
            if resp.status_code >= 500:
                logging.warning("Server error %s, retrying %s/%s", resp.status_code, attempt, retries)
                continue
            return resp
        except Exception as exc:  # pragma: no cover - network failure path
            logging.warning("Request error %s/%s: %s", attempt, retries, exc)
    return None
