"""Decorators for measuring performance of pipeline steps."""

import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def measure_performance(func):
    """Decorator to log execution time of a function."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            "Function %s executed in %.4f seconds", func.__name__, execution_time
        )
        return result

    return wrapper
