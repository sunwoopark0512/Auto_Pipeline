# Auto Pipeline

This repository contains scripts for generating marketing hooks using OpenAI, collecting keyword data, and uploading the results to Notion.

## Environment Variables

The scripts rely on several environment variables. Create a `.env` file or set them in your shell before running the pipeline.

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | API key used to access OpenAI. |
| `NOTION_API_TOKEN` | Token for authenticating with the Notion API. |
| `NOTION_HOOK_DB_ID` | ID of the Notion database that stores generated hooks. |
| `NOTION_KPI_DB_ID` | ID of the Notion database used for KPI statistics. |
| `NOTION_DB_ID` | ID of the Notion database for raw keyword uploads. |
| `HOOK_OUTPUT_PATH` | Path to save generated hook JSON. Default: `data/generated_hooks.json`. |
| `FAILED_HOOK_PATH` | Path to store hooks that failed to generate. Default: `logs/failed_hooks.json`. |
| `KEYWORD_OUTPUT_PATH` | Output JSON produced by the keyword pipeline. |
| `FAILED_UPLOADS_PATH` | File for keywords that failed to upload. |
| `UPLOADED_CACHE_PATH` | Cache file tracking uploaded keywords. |
| `TOPIC_CHANNELS_PATH` | JSON file describing topic channels. |
| `REPARSED_OUTPUT_PATH` | File used when retrying failed uploads. |
| `API_DELAY` | Delay between OpenAI API calls. |
| `UPLOAD_DELAY` | Delay between Notion upload requests. |
| `RETRY_DELAY` | Delay between retry attempts. |

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running Tests

Execute unit tests using `pytest` from the repository root:

```bash
pytest
```

The test suite covers prompt generation, text parsing, and retry logic.
