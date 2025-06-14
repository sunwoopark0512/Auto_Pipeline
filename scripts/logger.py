"""Utility for JSON-formatted logging."""

import json
import logging
from logging import Logger
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    """Simple formatter that outputs log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
        }
        extra = getattr(record, "extra", None)
        if isinstance(extra, dict):
            base.update(extra)
        return json.dumps(base)


def setup_logger(name: str) -> Logger:
    """Return a logger emitting JSON-formatted records."""

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
