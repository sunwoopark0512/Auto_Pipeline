import time
import logging
from typing import Callable, Iterable, Type, Optional, Any


def retry_with_backoff(
    fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 1.0,
    exceptions: Iterable[Type[BaseException]] = (Exception,),
    logger: Optional[logging.Logger] = None,
) -> Any:
    """Call ``fn`` with retries and exponential backoff."""
    for attempt in range(1, max_retries + 1):
        try:
            return fn()
        except tuple(exceptions) as error:
            if logger:
                logger.warning("Attempt %s/%s failed: %s", attempt, max_retries, error)
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** (attempt - 1))
            time.sleep(delay)

