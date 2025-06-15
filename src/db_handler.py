import os
import logging
import psycopg2
from psycopg2 import sql

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def get_db_connection():
    """Create a database connection using environment variables."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "your_db_name"),
        user=os.getenv("DB_USER", "your_user"),
        password=os.getenv("DB_PASSWORD", "your_password"),
        host=os.getenv("DB_HOST", "your_host"),
        port=os.getenv("DB_PORT", "your_port"),
    )


def update_db_status(step_name: str, status: str, error_details: str | None = None) -> None:
    """Insert a pipeline status record into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = sql.SQL(
            """
            INSERT INTO pipeline_status (step_name, status, error_details, timestamp)
            VALUES (%s, %s, %s, NOW())
            """
        )
        cursor.execute(query, (step_name, status, error_details))
        conn.commit()
        logger.info("DB status updated for %s with status %s", step_name, status)
    except Exception as exc:  # pragma: no cover - log-only path
        logger.error("Failed to update DB status for %s: %s", step_name, exc, exc_info=True)
    finally:
        cursor.close()
        conn.close()

