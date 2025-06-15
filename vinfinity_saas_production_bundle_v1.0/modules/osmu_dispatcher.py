from modules.uploader_youtube_shorts import upload_youtube_shorts
from modules.uploader_tiktok import upload_tiktok_video
from modules.uploader_tistory import upload_tistory_post
import os


def dispatch_to_platforms(title, full_text, slug, token):
    """Dispatch content to multiple platforms."""
    # YouTube Shorts
    upload_youtube_shorts(title, full_text[:1000], f"media/{slug}.mp4")
    # TikTok
    upload_tiktok_video(title, f"media/{slug}.mp4")
    # Tistory
    upload_tistory_post(os.getenv("TISTORY_BLOG"), title, full_text)
    # Additional platforms handled elsewhere
