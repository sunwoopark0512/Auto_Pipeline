import os
import time
import requests
import psycopg2
from dotenv import load_dotenv
from db_utils import get_conn

load_dotenv()

INTERVAL = int(os.getenv("ANALYTICS_INTERVAL_SEC", "1800"))


def fetch_wp_stats(post_id: str, token: str) -> dict:
    url = f"https://public-api.wordpress.com/rest/v1.1/sites/$YOUR_SITE_ID/posts/{post_id}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    j = resp.json()
    return {"views": j.get("views", 0), "likes": j.get("likes", 0)}


def save_metrics(content_id: str, platform: str, metrics: dict) -> None:
    with get_conn() as conn, conn.cursor() as cur:
        for k, v in metrics.items():
            cur.execute(
                """
              INSERT INTO analytics_log (content_id, platform, metric, value)
              VALUES (%s,%s,%s,%s)
            """,
                (content_id, platform, k, v),
            )
        conn.commit()


while True:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
          SELECT id, title->>'rendered' AS title, meta->>'wordpress_id' AS wp_id
          FROM content_tracker
          WHERE status='published'
        """
        )
        for content_id, title, wp_id in cur.fetchall():
            if not wp_id:
                continue
            token = os.getenv("WORDPRESS_API_TOKEN", "")
            metrics = fetch_wp_stats(wp_id, token)
            save_metrics(content_id, "wordpress", metrics)
            print(f"\U0001F4CA {title} → {metrics}")
    time.sleep(INTERVAL)
