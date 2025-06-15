import os
import json
import time
import logging
from typing import Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()

HOOK_JSON_PATH = os.getenv("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
UPLOAD_DELAY = float(os.getenv("UPLOAD_DELAY", "0.5"))

WORDPRESS_URL = os.getenv("WORDPRESS_API_URL")
WORDPRESS_TOKEN = os.getenv("WORDPRESS_API_TOKEN")
MEDIUM_URL = os.getenv("MEDIUM_API_URL")
MEDIUM_TOKEN = os.getenv("MEDIUM_API_TOKEN")
TWITTER_URL = os.getenv("TWITTER_API_URL")
TWITTER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
YOUTUBE_URL = os.getenv("YOUTUBE_API_URL")
YOUTUBE_TOKEN = os.getenv("YOUTUBE_API_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def _post(url: str, token: str, payload: Dict[str, Any]) -> None:
    if not url or not token:
        logging.warning("Missing URL or token; skipping upload")
        return
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("Upload success: %s", url)
    except Exception as exc:
        logging.error("Upload failed to %s: %s", url, exc)

def post_to_wordpress(hook: Dict[str, Any]) -> None:
    payload = {
        "title": hook.get("keyword"),
        "content": "\n".join(hook.get("blog_paragraphs", [])),
        "status": "draft",
    }
    _post(f"{WORDPRESS_URL}/posts", WORDPRESS_TOKEN, payload)

def post_to_medium(hook: Dict[str, Any]) -> None:
    payload = {
        "title": hook.get("keyword"),
        "contentFormat": "html",
        "content": "<p>" + "</p><p>".join(hook.get("blog_paragraphs", [])) + "</p>",
        "publishStatus": "draft",
    }
    _post(f"{MEDIUM_URL}/posts", MEDIUM_TOKEN, payload)

def post_to_twitter(hook: Dict[str, Any]) -> None:
    payload = {"text": hook.get("hook_lines", [""])[0]}
    _post(f"{TWITTER_URL}/tweets", TWITTER_TOKEN, payload)

def post_to_youtube(hook: Dict[str, Any]) -> None:
    payload = {
        "snippet": {"title": hook.get("video_titles", ["Untitled"])[0]},
        "status": {"privacyStatus": "private"},
    }
    _post(f"{YOUTUBE_URL}/videos", YOUTUBE_TOKEN, payload)

def upload_all_hooks() -> None:
    if not os.path.exists(HOOK_JSON_PATH):
        logging.error("Hook JSON not found: %s", HOOK_JSON_PATH)
        return
    with open(HOOK_JSON_PATH, "r", encoding="utf-8") as fh:
        hooks = json.load(fh)
    total = 0
    for hook in hooks:
        total += 1
        post_to_wordpress(hook)
        post_to_medium(hook)
        post_to_twitter(hook)
        post_to_youtube(hook)
        time.sleep(UPLOAD_DELAY)
    logging.info("Uploaded hooks to all platforms: %d", total)

if __name__ == "__main__":
    upload_all_hooks()
