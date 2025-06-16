import os
import json
import time
import logging
from dotenv import load_dotenv

load_dotenv()

HOOK_JSON_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BLOG_API_TOKEN = os.getenv("BLOG_API_TOKEN")
SNS_API_TOKEN = os.getenv("SNS_API_TOKEN")
UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "0.5"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def upload_to_youtube(item):
    """Stub for uploading content to YouTube."""
    if not YOUTUBE_API_KEY:
        logging.debug("YouTube API 키가 설정되지 않아 스킵합니다.")
        return
    logging.info(f"[YouTube] Uploading video for keyword '{item['keyword']}' (stub)")
    # 실제 구현에서는 google-api-python-client 등을 이용하여 동영상 업로드 및 정보 등록을 수행합니다.


def upload_to_blog(item):
    """Stub for creating a blog post."""
    if not BLOG_API_TOKEN:
        logging.debug("Blog API 토큰이 설정되지 않아 스킵합니다.")
        return
    logging.info(f"[Blog] Posting article for keyword '{item['keyword']}' (stub)")
    # 실제 구현에서는 블로그 플랫폼 API를 호출하여 게시글을 생성합니다.


def upload_to_sns(item):
    """Stub for posting summary to SNS."""
    if not SNS_API_TOKEN:
        logging.debug("SNS API 토큰이 설정되지 않아 스킵합니다.")
        return
    summary = item.get("sns_summary") or " ".join(item.get("hook_lines", []))
    logging.info(f"[SNS] Posting: {summary[:60]}... (stub)")
    # 실제 구현에서는 Twitter API 등 SNS API를 호출하여 포스팅합니다.


def upload_all_channels():
    if not os.path.exists(HOOK_JSON_PATH):
        logging.error(f"❌ 후킹 결과 파일이 없습니다: {HOOK_JSON_PATH}")
        return

    with open(HOOK_JSON_PATH, 'r', encoding='utf-8') as f:
        hooks = json.load(f)

    for item in hooks:
        upload_to_youtube(item)
        upload_to_blog(item)
        upload_to_sns(item)
        time.sleep(UPLOAD_DELAY)

    logging.info("✅ 채널별 업로드(스텁) 완료")


if __name__ == "__main__":
    upload_all_channels()
