import logging
from .db_handler import update_db_status

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def generate_content(topic: str, language: str):
    """Generate dummy content for a topic."""
    try:
        content = {
            "title": f"Generated content for {topic}",
            "body": f"Content generated in {language} language."
        }
        update_db_status("Content Generation", "Success")
        return content
    except Exception as exc:  # pragma: no cover - log-only path
        update_db_status("Content Generation", "Failed", str(exc))
        logger.error("Error generating content: %s", exc, exc_info=True)
        return None
