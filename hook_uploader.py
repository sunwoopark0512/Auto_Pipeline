from typing import Tuple

def upload_to_wordpress(title: str, content: str, slug: str, token: str) -> Tuple[str, int]:
    """Stub uploader that returns success."""
    print(f"Uploading '{title}' with slug '{slug}'")
    return "success", 1
