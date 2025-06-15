import os
import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_conn():
    conn = psycopg2.connect(
        host=os.getenv("SUPABASE_HOST", "localhost"),
        port=os.getenv("SUPABASE_PORT", "5432"),
        dbname=os.getenv("SUPABASE_DB", "supabase"),
        user=os.getenv("SUPABASE_USER", "postgres"),
        password=os.getenv("SUPABASE_PASSWORD", "postgres"),
    )
    try:
        yield conn
    finally:
        conn.close()


def record_content(user_id, keyword, content, status):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO content_tracker (user_id, keyword, title, content, status)
            VALUES (%s,%s,%s,%s,%s)
        """,
            (user_id, keyword, keyword, content, status),
        )
        conn.commit()


def get_content_count(user_id):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM content_tracker WHERE user_id=%s", (user_id,))
        return cur.fetchone()[0]
