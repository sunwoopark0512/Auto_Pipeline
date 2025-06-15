"""Utility to upload generated content to WordPress."""

import requests  # pylint: disable=import-error


def upload_to_wordpress(title: str, content: str, slug: str, token: str):
    """Upload a post to WordPress via REST API.

    Args:
        title: Post title.
        content: Post content in HTML or Markdown.
        slug: URL slug for the post.
        token: Bearer token for authentication.

    Returns:
        Tuple of status code and JSON response from the API.
    """
    endpoint = "https://yourblog.com/wp-json/wp/v2/posts"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "publish",
    }
    response = requests.post(endpoint, headers=headers, json=data)
    return response.status_code, response.json()
