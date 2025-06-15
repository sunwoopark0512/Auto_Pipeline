import os
import time

from super_orchestrator import run_pipeline
from billing_utils import check_user_quota
from db_utils import get_conn

INTERVAL_SEC = int(os.getenv("SCHEDULER_INTERVAL", "60"))

while True:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, topic, user_id
            FROM scheduler_queue
            WHERE status='scheduled'
            ORDER BY scheduled_at ASC
            LIMIT 1
        """
        )
        row = cur.fetchone()

        if row:
            queue_id, topic, user_id = row
            try:
                check_user_quota(user_id)
                print(f"▶︎ Running queued job «{topic}» for user {user_id}")
                run_pipeline(topic, os.getenv("WORDPRESS_API_TOKEN"))
                cur.execute(
                    "UPDATE scheduler_queue SET status='completed' WHERE id=%s",
                    (queue_id,),
                )
            except Exception as e:
                cur.execute(
                    "UPDATE scheduler_queue SET status='failed' WHERE id=%s", (queue_id,)
                )
                print("⚠️  Job failed:", e)
            conn.commit()
    time.sleep(INTERVAL_SEC)
