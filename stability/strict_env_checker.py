"""Ensure required environment variables exist before execution."""

import os
import sys

REQUIRED_VARS = ["NOTION_TOKEN", "SUPABASE_KEY", "OPENAI_API_KEY"]
missing = [k for k in REQUIRED_VARS if not os.getenv(k)]

if missing:
    print(f"❌ Missing env vars: {missing}")
    sys.exit(1)
