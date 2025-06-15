import requests, os, hashlib, time, hmac, json


def upload_tiktok_video(title: str, filepath: str):
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    open_id = os.getenv("TIKTOK_OPEN_ID")

    # 1. 비디오 파일 업로드 (pre-upload)
    upload_url = "https://open.tiktokapis.com/v2/video/upload/"
    with open(filepath, "rb") as f:
        video = f.read()
    headers = {"access-token": access_token}
    resp = requests.post(upload_url, headers=headers, files={"video": video})
    video_id = resp.json()["data"]["video"]["video_id"]

    # 2. 게시물 생성
    publish_url = "https://open.tiktokapis.com/v2/video/publish/"
    data = {"video_id": video_id, "open_id": open_id, "text": title}
    resp2 = requests.post(publish_url, headers=headers, json=data)
    return resp2.json()
