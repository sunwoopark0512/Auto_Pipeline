import os
from dotenv import load_dotenv

load_dotenv()

class ConfigError(Exception):
    """Raised when a required environment variable is missing or invalid."""
    pass


def get_env(name: str, default=None, *, cast=None):
    value = os.getenv(name, default)
    if cast and value is not None:
        try:
            value = cast(value)
        except (ValueError, TypeError):
            raise ConfigError(f"Invalid value for environment variable '{name}': {value}")
    return value

# File paths and tokens
TOPIC_CHANNELS_PATH = get_env("TOPIC_CHANNELS_PATH", "config/topic_channels.json")
KEYWORD_OUTPUT_PATH = get_env("KEYWORD_OUTPUT_PATH", "data/keyword_output_with_cpc.json")
HOOK_OUTPUT_PATH = get_env("HOOK_OUTPUT_PATH", "data/generated_hooks.json")
FAILED_HOOK_PATH = get_env("FAILED_HOOK_PATH", "logs/failed_hooks.json")
REPARSED_OUTPUT_PATH = get_env("REPARSED_OUTPUT_PATH", "logs/failed_keywords_reparsed.json")
UPLOADED_CACHE_PATH = get_env("UPLOADED_CACHE_PATH", "data/uploaded_keywords_cache.json")
FAILED_UPLOADS_PATH = get_env("FAILED_UPLOADS_PATH", "logs/failed_uploads.json")

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
NOTION_API_TOKEN = get_env("NOTION_API_TOKEN")
NOTION_DB_ID = get_env("NOTION_DB_ID")
NOTION_HOOK_DB_ID = get_env("NOTION_HOOK_DB_ID")
NOTION_KPI_DB_ID = get_env("NOTION_KPI_DB_ID")

# Numeric settings
UPLOAD_DELAY = get_env("UPLOAD_DELAY", 0.5, cast=float)
RETRY_DELAY = get_env("RETRY_DELAY", 0.5, cast=float)
API_DELAY = get_env("API_DELAY", 1.0, cast=float)


def require(*names: str) -> None:
    """Ensure the given env vars are present and not empty."""
    missing = [n for n in names if globals().get(n) in (None, "")]
    if missing:
        raise ConfigError("Missing required environment variables: " + ", ".join(missing))
