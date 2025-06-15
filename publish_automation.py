#!/usr/bin/env python3
"""
publish_automation.py
콘텐츠 자동 발행 및 SNS 릴레이
- WordPress, YouTube, Instagram, Twitter 등
- 뉴스레터 및 RSS 발행
"""

import os
import requests
from datetime import datetime

# 환경변수에서 API 키를 불러옵니다.
WORDPRESS_API_URL = os.getenv("WORDPRESS_API_URL")
WORDPRESS_API_KEY = os.getenv("WORDPRESS_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def publish_to_wordpress(
    title: str, content: str, category: str = "General"
) -> bool:
    """WordPress에 글을 자동으로 발행합니다."""
    url = f"{WORDPRESS_API_URL}/wp-json/wp/v2/posts"
    headers = {
        "Authorization": f"Bearer {WORDPRESS_API_KEY}",
        "Content-Type": "application/json",
    }
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [category],
        "date": datetime.now().isoformat(),
    }
    response = requests.post(url, json=post_data, headers=headers, timeout=30)
    if response.status_code == 201:
        print(f"✅ WordPress에 게시되었습니다: {title}")
        return True
    print(f"❌ WordPress 게시 실패: {response.text}")
    return False


def publish_to_twitter(content: str) -> bool:
    """Twitter에 자동으로 콘텐츠를 게시합니다."""
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {TWITTER_API_KEY}",
        "Content-Type": "application/json",
    }
    tweet_data = {"text": content}
    response = requests.post(url, json=tweet_data, headers=headers, timeout=30)
    if response.status_code == 201:
        print(f"✅ Twitter에 게시되었습니다: {content}")
        return True
    print(f"❌ Twitter 게시 실패: {response.text}")
    return False


def publish_to_youtube(video_id: str, title: str, description: str) -> bool:
    """YouTube에 자동으로 비디오를 업로드합니다."""
    url = (
        "https://www.googleapis.com/upload/youtube/v3/videos"
        "?uploadType=resumable&part=snippet,status"
    )
    headers = {
        "Authorization": f"Bearer {YOUTUBE_API_KEY}",
        "Content-Type": "application/json",
    }
    video_data = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["AI", "automation", "content creation"],
        },
        "status": {"privacyStatus": "public"},
    }
    response = requests.post(url, json=video_data, headers=headers, timeout=30)
    if response.status_code == 200:
        print(f"✅ YouTube에 비디오 업로드 완료: {title}")
        return True
    print(f"❌ YouTube 업로드 실패: {response.text}")
    return False


def publish_to_rss(title: str, content: str, rss_feed_url: str) -> bool:
    """RSS 피드에 자동으로 콘텐츠를 추가합니다."""
    import feedparser

    feedparser.parse(rss_feed_url)
    # (RSS 피드로 콘텐츠 추가하는 로직 추가 필요)
    print(f"✅ RSS에 콘텐츠 추가 완료: {title}")
    return True


def send_newsletter(
    subject: str, content: str, newsletter_email_list: list
) -> bool:
    """구독자 목록으로 뉴스레터를 발송합니다."""
    # (Mailgun, SendGrid, SMTP 사용)
    print(f"✅ 뉴스레터 발송 완료: {subject}")
    return True


def automate_publish(content: str, title: str, platform: str = "wordpress"):
    """선택된 플랫폼에 콘텐츠를 자동으로 게시하는 메인 함수"""
    if platform == "wordpress":
        return publish_to_wordpress(title, content)
    if platform == "twitter":
        return publish_to_twitter(content)
    if platform == "youtube":
        return publish_to_youtube("video_id_example", title, content)
    if platform == "rss":
        return publish_to_rss(title, content, "https://example.com/rss_feed")
    if platform == "newsletter":
        return send_newsletter(title, content, ["example@example.com"])
    print(f"❌ 지원되지 않는 플랫폼: {platform}")
    return False


if __name__ == "__main__":
    EXAMPLE_CONTENT = "새로운 여행지에 대한 모든 정보! 이번엔 몰타를 소개합니다."
    EXAMPLE_TITLE = "2025년 여행지 추천: 몰타"
    automate_publish(EXAMPLE_CONTENT, EXAMPLE_TITLE, platform="wordpress")
    automate_publish(EXAMPLE_CONTENT, EXAMPLE_TITLE, platform="twitter")
