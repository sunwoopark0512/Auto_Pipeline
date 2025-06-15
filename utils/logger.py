import logging
import os

def setup_logging(log_file: str = "logs/app.log", level: int = logging.INFO) -> logging.Logger:
    """Configure root logger to log to console and a file with uniform format.

    Parameters
    ----------
    log_file : str
        Path to the log file.
    level : int
        Logging level.

    Returns
    -------
    logging.Logger
        Configured root logger instance.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")

    # Prevent duplicate handlers in case of multiple calls
    if logger.handlers:
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
