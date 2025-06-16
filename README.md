# Auto_Pipeline

Automation pipeline for generating content and uploading to Notion.

## Components
- `hook_generator.py` – generates hooks using OpenAI.
- `keyword_auto_pipeline.py` – collects trending keywords.
- `notion_hook_uploader.py` – uploads generated hooks to Notion.
- `security_utils.py` – utilities for encryption, JWT authentication and privacy management.

For usage, run `python run_pipeline.py`.
