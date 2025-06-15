import os
import psycopg2
import numpy as np
from psycopg2.extras import register_vector

DB_URL = os.getenv('RAG_DB_URL', 'dbname=vinfinity')

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

register_vector(conn)


def update_vector_feedback(doc_id: int, feedback_score: float) -> None:
    """Update vector embedding with feedback weight."""
    cur.execute("SELECT embedding FROM rag_store WHERE id=%s", (doc_id,))
    row = cur.fetchone()
    if not row:
        raise ValueError(f"doc_id {doc_id} not found")
    vec = np.array(row[0])
    adjusted = vec * (1 + feedback_score * 0.05)
    cur.execute("UPDATE rag_store SET embedding=%s WHERE id=%s", (list(adjusted), doc_id))
    conn.commit()

