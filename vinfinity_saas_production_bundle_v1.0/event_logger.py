import json
from db_utils import get_conn


def log_event(user_id, event, **meta):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
          INSERT INTO event_log (user_id, event, meta)
          VALUES (%s,%s,%s)
        """,
            (user_id, event, json.dumps(meta)),
        )
        conn.commit()
