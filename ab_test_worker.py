"""Worker that enqueues A/B test variants for published content."""
import time
from db_utils import get_conn
from ab_test_generator import generate_variants


while True:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
          SELECT id, title, user_id
          FROM content_tracker
          WHERE status='published' AND ab_test_done IS NOT TRUE
          LIMIT 1
        """
        )
        row = cur.fetchone()
        if row:
            cid, title, user = row
            variants = generate_variants(title, 2)
            for label, text in zip(["A", "B"], variants):
                cur.execute(
                    """
                  INSERT INTO ab_test_queue (content_id, variant, field, original, variant_text)
                  VALUES (%s,%s,'title',%s,%s)
                """,
                    (cid, label, title, text),
                )
            cur.execute("UPDATE content_tracker SET ab_test_done=TRUE WHERE id=%s", (cid,))
            conn.commit()
    time.sleep(300)
