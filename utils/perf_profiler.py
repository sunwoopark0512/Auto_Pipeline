"""Simple performance profiling utilities."""
from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Callable, TypeVar


F = TypeVar("F", bound=Callable)


def timeit(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore[misc]
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logging.info("%s took %.2fs", func.__name__, duration)
        return result

    return wrapper  # type: ignore[return-value]

