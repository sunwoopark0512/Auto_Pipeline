"""Channel-specific uploader plugin classes."""

from __future__ import annotations

import os
import pathlib
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple

# ─────────────────── 공표 인터페이스 ──────────────────── #


class BaseUploader(ABC):
    """Every uploader returns (remote_id, public_url)."""

    @abstractmethod
    def upload(self, row: Dict[str, Any]) -> Tuple[str, str]:
        raise NotImplementedError


# ──────────────────── YouTube ──────────────────── #
class YouTubeUploader(BaseUploader):
    """Uploader using YouTube Data API v3 (refresh-token flow)."""

    def __init__(self):
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.oauth2.credentials import Credentials

        creds_path = pathlib.Path(os.getenv("YT_CREDENTIALS_FILE", "yt_credentials.json"))
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        if creds_path.exists():
            creds = Credentials.from_authorized_user_file(creds_path, scopes)
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
            creds = flow.run_console()
            creds_path.write_text(creds.to_json())

        self.service = build("youtube", "v3", credentials=creds, cache_discovery=False)

    def upload(self, row: Dict[str, Any]):
        body = {
            "snippet": {"title": row["title"], "description": row["content"][:4900]},
            "status": {"privacyStatus": "public"},
        }
        media_file = row.get("video_path")  # 로컬 파일 경로
        if not media_file:
            raise ValueError("Missing video_path for YouTube upload")

        request = self.service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media_file,
        )
        response = request.execute()
        return response["id"], f"https://youtu.be/{response['id']}"


# ──────────────────── Medium ──────────────────── #
class MediumUploader(BaseUploader):
    def __init__(self):
        self.token = os.getenv("MEDIUM_TOKEN")
        self.user_id = self._get_user_id()

    def _get_user_id(self) -> str:
        r = requests.get(
            "https://api.medium.com/v1/me",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=20,
        )
        r.raise_for_status()
        return r.json()["data"]["id"]

    def upload(self, row):
        r = requests.post(
            f"https://api.medium.com/v1/users/{self.user_id}/posts",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            json={
                "title": row["title"],
                "contentFormat": "html",
                "content": row["content_html"] or row["content"],
                "publishStatus": "public",
            },
            timeout=30,
        )
        r.raise_for_status()
        post = r.json()["data"]
        return post["id"], post["url"]


# ─────────────── X(Twitter) ─────────────── #
class XUploader(BaseUploader):
    def __init__(self):
        self.bearer = os.getenv("X_BEARER_TOKEN")

    def upload(self, row):
        text = (row["content"][:275] + "…") if len(row["content"]) > 280 else row["content"]
        r = requests.post(
            "https://api.twitter.com/2/tweets",
            headers={"Authorization": f"Bearer {self.bearer}", "Content-Type": "application/json"},
            json={"text": text},
            timeout=15,
        )
        r.raise_for_status()
        tid = r.json()["data"]["id"]
        return tid, f"https://x.com/i/web/status/{tid}"


# ─────────────── Tistory (Selenium) ─────────────── #
class TistoryUploader(BaseUploader):
    """간단히 Selenium으로 자동화 (API 없이)."""

    def __init__(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_opts = Options()
        chrome_opts.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=chrome_opts)
        self.url = "https://www.tistory.com/"

    def upload(self, row):
        # 로그인 / 게시글 작성 자동화 예시(단축) – 실제 권은 사이트 구조에 맞게 조정
        d = self.driver
        d.get(self.url)
        # … (login, editor 작성, publish) …
        post_url = d.current_url  # 마지막 게시 건너려 후 URL
        return "tistory-id", post_url
