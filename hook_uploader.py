def upload_to_wordpress(title: str, content: str, slug: str, token: str):
    """Return a fake upload status and response."""
    return 201, {"title": title, "slug": slug}
