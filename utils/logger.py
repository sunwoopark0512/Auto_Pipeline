import logging
import os
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger with console and file handlers.

    The log level and file path can be controlled with environment variables
    LOG_LEVEL and LOG_FILE. Default level is INFO and file is logs/app.log.
    """
    logger = logging.getLogger(name) if name else logging.getLogger()
    if logger.handlers:
        return logger

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_file = os.getenv("LOG_FILE", "logs/app.log")

    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.setLevel(getattr(logging, log_level, logging.INFO))
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
