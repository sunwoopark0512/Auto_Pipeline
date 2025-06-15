from fastapi import FastAPI, Body
from db_utils import get_conn

app = FastAPI()


@app.post("/feedback")
def submit_feedback(trace_id: str = Body(), rating: int = Body(..., gt=0, lt=6)):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
          INSERT INTO llm_feedback(trace_id, rating) VALUES(%s,%s)
        """,
            (trace_id, rating),
        )
        conn.commit()
    return {"status": "ok"}
