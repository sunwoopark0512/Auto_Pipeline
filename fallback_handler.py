"""Utilities for handling fallback behavior when pipeline steps fail."""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)


def handle_fallback(failed_step: str, error_details: str) -> None:
    """Handle fallback logic when a step fails."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.warning(
        "[%s] Fallback triggered for step: %s | Error: %s",
        timestamp,
        failed_step,
        error_details,
    )
    try:
        # Placeholder for recovery logic such as DB updates or notifications
        pass
    except Exception as exc:  # pragma: no cover - fallback rarely fails
        logger.error("Fallback for %s failed: %s", failed_step, exc, exc_info=True)
