"""Upload generated hooks to WordPress via REST API."""

import requests


def upload_to_wordpress(title: str, content: str, slug: str, token: str):
    """Publish a post to WordPress and return status information."""
    endpoint = "https://yourwordpress.com/wp-json/wp/v2/posts"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "publish"
    }
    response = requests.post(endpoint, headers=headers, json=data, timeout=10)
    return response.status_code, response.json()
