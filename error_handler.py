import logging
from datetime import datetime

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def log_error(error_message: str, error_details: str | None = None) -> None:
    """Log an error with optional details and timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if error_details:
        error_message = f"{error_message} | Details: {error_details}"
    logger.error(f"[{timestamp}] {error_message}")
