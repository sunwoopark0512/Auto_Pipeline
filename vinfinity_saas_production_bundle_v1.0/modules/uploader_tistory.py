import requests, os


def upload_tistory_post(blog_name: str, title: str, content: str, category: int = 0, visibility: int = 3):
    token = os.getenv("TISTORY_TOKEN")
    endpoint = f"https://www.tistory.com/apis/post/write?access_token={token}"
    data = {
        "blogName": blog_name,
        "title": title,
        "content": content,
        "category": category,
        "visibility": visibility,
        "output": "json",
    }
    resp = requests.post(endpoint, data=data)
    return resp.json()
