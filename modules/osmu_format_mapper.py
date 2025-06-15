PLATFORM_LIMITS = {
    "instagram": {"max_text": 2200},
    "twitter":   {"max_text": 280},
    "linkedin":  {"max_text": 3000},
    "youtube":   {"max_text": 5000},
}

def get_limits(platform: str) -> dict:
    return PLATFORM_LIMITS.get(platform, {"max_text": 1000})
