import os
from dotenv import load_dotenv

load_dotenv()

# Use FAILED_HOOK_PATH as the unified environment variable.
# For backward compatibility, fall back to REPARSED_OUTPUT_PATH if provided.
FAILED_HOOK_PATH = os.getenv(
    "FAILED_HOOK_PATH",
    os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_hooks.json")
)
