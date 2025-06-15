from fastapi import FastAPI, HTTPException
from db_utils import get_conn

app = FastAPI()

@app.delete("/user/{user_id}")
def delete_user(user_id: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM event_log WHERE user_id=%s", (user_id,))
        cur.execute("DELETE FROM conversion_log WHERE user_id=%s", (user_id,))
        conn.commit()
    return {"status":"deleted"}
