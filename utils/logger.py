import logging
import os
from typing import Optional


def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger.

    Log level and file are controlled by environment variables LOG_LEVEL and
    LOG_FILE. Defaults to INFO level and console output only.
    """
    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    log_file = os.getenv("LOG_FILE")

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s:%(message)s", handlers=handlers)
    return logging.getLogger(name)
