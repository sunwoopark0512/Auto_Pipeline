import os
import psycopg2
from contextlib import contextmanager


@contextmanager
def get_conn():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")
    conn = psycopg2.connect(dsn)
    try:
        yield conn
    finally:
        conn.close()
