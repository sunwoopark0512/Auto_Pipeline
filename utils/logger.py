import logging
import os
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a logger configured with consistent handlers and format.

    Logging destination is controlled via environment variables:
    - LOG_TO_FILE: if '1', logs are written to a file.
    - LOG_FILE_PATH: path to log file (default 'logs/app.log').
    - LOG_LEVEL: logging level (default 'INFO').
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Logger already configured
        return logger

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_to_file = os.getenv("LOG_TO_FILE", "0") == "1"
    log_file_path = os.getenv("LOG_FILE_PATH", "logs/app.log")

    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")

    if log_to_file:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
