"""Billing utilities for quota checks."""

from auth_utils import get_user_profile


def get_content_count(_user_id: int) -> int:
    """Placeholder for content count retrieval for a user."""

    # In actual implementation, this would query a database or service
    return 0


def check_user_quota(user_id):
    """Ensure ``user_id`` has remaining content generation quota."""

    plan, _ = get_user_profile(user_id)
    limit = {"free": 10, "starter": 100, "pro": 1000}[plan]
    current_count = get_content_count(user_id)
    if current_count >= limit:
        raise Exception("Quota exceeded")
