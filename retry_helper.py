import time
import random
import logging
from typing import Any, Callable, Tuple, Optional


def call_with_backoff(func: Callable[..., Any], *args: Any, max_retries: int = 3,
                      base_delay: float = 1.0, logger: Optional[logging.Logger] = None,
                      **kwargs: Any) -> Tuple[Optional[Any], Optional[dict]]:
    """Call a function with exponential backoff retry.

    Returns a tuple of (result, error_info). On success error_info is None.
    error_info contains the exception string and attempt count.
    """
    delay = base_delay
    for attempt in range(1, max_retries + 1):
        try:
            result = func(*args, **kwargs)
            return result, None
        except Exception as e:  # pylint: disable=broad-except
            if logger:
                logger.error("%s failed on attempt %s/%s: %s", func.__name__, attempt, max_retries, e)
            if attempt == max_retries:
                return None, {"error": str(e), "attempts": attempt}
            time.sleep(delay * (1 + random.random()))
            delay *= 2
    return None, {"error": "Unknown", "attempts": max_retries}
