import os, googleapiclient.discovery, googleapiclient.http


def upload_youtube_shorts(title: str, description: str, filepath: str):
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets = os.getenv("YT_CLIENT_SECRET_FILE", "client_secret.json")

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets, scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    creds = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)

    body = {
        "snippet": {"title": title, "description": description, "tags": ["#Shorts"]},
        "status": {"privacyStatus": "public"},
    }
    media = googleapiclient.http.MediaFileUpload(filepath, chunksize=-1, resumable=True)

    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = req.execute()
    return resp.get("id")
