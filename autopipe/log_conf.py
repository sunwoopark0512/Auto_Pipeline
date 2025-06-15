"""Logging configuration used across the project."""

LOG_CFG = {
    "version": 1,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "INFO"},
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/pipeline.log",
            "when": "midnight",
            "backupCount": 7,
            "level": "DEBUG",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "INFO"},
}
