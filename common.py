import os
from dotenv import load_dotenv

load_dotenv()

# Unified path for failed hook uploads
FAILED_HOOK_PATH = os.getenv("FAILED_HOOK_PATH") or os.getenv("REPARSED_OUTPUT_PATH", "logs/failed_keywords.json")
