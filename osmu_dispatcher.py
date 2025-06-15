from ffmpeg_renderer import render_short


def upload_youtube_shorts(title: str, description: str, video_path: str) -> None:
    """Placeholder for YouTube Shorts upload logic."""
    pass


def upload_tiktok_video(title: str, video_path: str) -> None:
    """Placeholder for TikTok upload logic."""
    pass


def dispatch(title: str, full_text: str) -> None:
    # Shorts용 비디오 생성
    video_path = render_short(full_text[:200])
    upload_youtube_shorts(title, full_text[:1000], video_path)
    upload_tiktok_video(title, video_path)
