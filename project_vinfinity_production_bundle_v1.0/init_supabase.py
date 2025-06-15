"""Initialize the Supabase database with schema."""

import psycopg2


def init_db(dsn: str, schema_path: str) -> None:
    """Create tables using schema.sql."""
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = f.read()
    conn = psycopg2.connect(dsn)
    with conn, conn.cursor() as cur:
        cur.execute(schema)
    conn.close()
