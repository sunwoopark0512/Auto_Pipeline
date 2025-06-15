from flask import Flask, request
from db_utils import get_conn

app = Flask(__name__)


@app.route("/conversion", methods=["POST"])
def conversion():
    data = request.json
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
          INSERT INTO conversion_log (user_id, content_id, platform, revenue_cents, event)
          VALUES (%s,%s,%s,%s,%s)
        """,
            (
                data["user_id"],
                data["content_id"],
                data["platform"],
                data.get("revenue_cents", 0),
                data["event"],
            ),
        )
        conn.commit()
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
