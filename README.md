# Auto Pipeline

This repository contains a retry helper for uploading parsed keywords to Notion.

## Environment Variables

- `NOTION_API_TOKEN`: API token for Notion access.
- `NOTION_HOOK_DB_ID`: Database ID for the Notion page.
- `RETRY_DELAY`: Delay between retries in seconds.
- `REPARSED_OUTPUT_PATH`: Path to the JSON file storing items that failed to upload.

Create a `.env` file based on `.env.example` and provide the required values.
