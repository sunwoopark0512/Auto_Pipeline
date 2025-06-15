"""WordPress 게시 업로드 스크립트."""

import os
import json
import time
import logging
from dotenv import load_dotenv
import requests

# ---------------------- 환경 변수 로드 ----------------------
load_dotenv()
WORDPRESS_URL = os.getenv("WORDPRESS_URL")
WP_USERNAME = os.getenv("WORDPRESS_USERNAME")
WP_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")
CONTENT_PATH = os.getenv("CONTENT_OUTPUT_PATH", "data/optimized_content.json")
PUBLISH_DELAY = float(os.getenv("PUBLISH_DELAY", "1.0"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 게시물 업로드 함수 ----------------------
def publish_post(post):
    """하나의 게시물을 워드프레스에 업로드한다."""

    data = {
        "title": post.get("title"),
        "content": post.get("content"),
        "status": "publish",
    }
    response = requests.post(
        f"{WORDPRESS_URL}/wp-json/wp/v2/posts",
        auth=(WP_USERNAME, WP_APP_PASSWORD),
        json=data,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

# ---------------------- 전체 게시물 처리 ----------------------
def publish_all_posts():
    """콘텐츠 JSON을 읽어 모두 게시한다."""

    if not WORDPRESS_URL or not WP_USERNAME or not WP_APP_PASSWORD:
        logging.error("❗ WordPress 환경 변수 누락")
        return

    try:
        with open(CONTENT_PATH, "r", encoding="utf-8") as f:
            posts = json.load(f)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("❗ 콘텐츠 파일 읽기 오류: %s", e)
        return

    success = failed = 0
    for post in posts:
        title = post.get("title", "(제목 없음)")
        try:
            publish_post(post)
            logging.info("✅ 게시 완료: %s", title)
            success += 1
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("❌ 게시 실패: %s - %s", title, e)
            failed += 1
        time.sleep(PUBLISH_DELAY)

    logging.info("📊 워드프레스 업로드 요약: 총 %d | 성공 %d | 실패 %d", len(posts), success, failed)


if __name__ == "__main__":
    publish_all_posts()
