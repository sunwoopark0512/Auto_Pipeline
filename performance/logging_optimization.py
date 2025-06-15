"""Structured JSON logging configuration for Datadog/Cloud Logging."""

import json
import logging

logger = logging.getLogger("vinfinity")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        json.dumps(
            {"timestamp": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}
        )
    )
)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
