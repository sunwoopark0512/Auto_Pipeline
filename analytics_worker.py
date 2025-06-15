"""Simple analytics worker that records metrics and triggers rewriting."""
from typing import Dict
from db_utils import get_conn
from performance_rewriter import rewrite_for_performance


def save_metrics(content_id: str, metrics: Dict[str, int], title: str) -> None:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO analytics (content_id, views) VALUES (%s, %s)",
            (content_id, metrics.get("views", 0)),
        )
        if metrics.get("views", 0) < 100:
            new_title = rewrite_for_performance(title, "low views")
            cur.execute(
                """
      UPDATE ab_test_queue
      SET variant='R', field='title', original=%s, variant_text=%s
      WHERE content_id=%s
                """,
                (title, new_title, content_id),
            )
        conn.commit()
