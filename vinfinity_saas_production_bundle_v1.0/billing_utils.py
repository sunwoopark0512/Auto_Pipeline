from db_utils import get_content_count
from auth_utils import get_user_profile

PLAN_LIMITS = {"free": 10, "starter": 100, "pro": 1000}


def check_user_quota(user_id):
    plan, _ = get_user_profile(user_id)
    limit = PLAN_LIMITS.get(plan, 10)
    if get_content_count(user_id) >= limit:
        raise Exception(f"Quota exceeded for plan '{plan}'")
