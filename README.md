# Auto Pipeline

This repository contains a set of scripts that generate marketing hooks from trending keywords and uploads the results to Notion.  The project is designed to run both locally and via GitHub Actions.

## Installation

1. Install Python 3.10 or later.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(The `requirements.txt` file should contain packages such as `openai`, `notion-client`, `python-dotenv`, `pytrends`, and `snscrape`.)*

## Environment Variables

The project relies on several environment variables.  They can be placed in a `.env` file or set directly in your environment.

| Variable | Default | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | – | API key used by `hook_generator.py` |
| `NOTION_API_TOKEN` | – | Token for accessing Notion APIs |
| `NOTION_DB_ID` | – | Target database ID used by `scripts/notion_uploader.py` |
| `NOTION_HOOK_DB_ID` | – | Database for uploading generated hooks |
| `NOTION_KPI_DB_ID` | – | Dashboard database for retry statistics |
| `KEYWORD_OUTPUT_PATH` | `data/keyword_output_with_cpc.json` | Output file produced by `keyword_auto_pipeline.py` |
| `HOOK_OUTPUT_PATH` | `data/generated_hooks.json` | Output file produced by `hook_generator.py` |
| `FAILED_HOOK_PATH` | `logs/failed_hooks.json` | Failed hook items |
| `UPLOADED_CACHE_PATH` | `data/uploaded_keywords_cache.json` | Cache for uploaded keywords |
| `FAILED_UPLOADS_PATH` | `logs/failed_uploads.json` | Log of failed keyword uploads |
| `REPARSED_OUTPUT_PATH` | `logs/failed_keywords_reparsed.json` | Location for retry data |
| `TOPIC_CHANNELS_PATH` | `config/topic_channels.json` | Keyword topic list |
| `UPLOAD_DELAY` | `0.5` | Delay between Notion uploads (seconds) |
| `RETRY_DELAY` | `0.5` | Delay between retry attempts |
| `API_DELAY` | `1.0` | Delay between OpenAI API calls |

## Running Locally

1. Prepare a `.env` file with the required variables.
2. Execute the main pipeline:
   ```bash
   python run_pipeline.py
   ```
   The pipeline will sequentially run the scripts listed in `run_pipeline.py`.

### Individual Scripts

- `keyword_auto_pipeline.py` – Gathers trending keywords from Google Trends and Twitter, filters them, and saves a JSON file. Example output snippet:
  ```json
  {
    "timestamp": "2023-01-01T00:00:00Z",
    "filtered_keywords": [
      {"keyword": "여행 국내여행", "source": "GoogleTrends", "score": 78, "growth": 1.5, "cpc": 1500}
    ]
  }
  ```
- `hook_generator.py` – Generates marketing hooks using GPT and writes `data/generated_hooks.json`.
- `notion_hook_uploader.py` – Uploads generated hooks to Notion and records failures in `logs/`.
- `retry_failed_uploads.py` – Attempts to upload items that previously failed.
- `retry_dashboard_notifier.py` – Summarises retry statistics and sends them to a Notion KPI dashboard.

## GitHub Actions

The workflow file [`daily-pipeline.yml.txt`](.github/workflows/daily-pipeline.yml.txt) schedules the pipeline every day at 00:00 UTC.  The job installs dependencies, runs `scripts/run_pipeline.py`, and uploads any failed items as artifacts.  Required secrets such as `OPENAI_API_KEY` and `NOTION_API_TOKEN` must be configured in the repository settings.


### Sample `generated_hooks.json`
```json
[
  {
    "keyword": "여행 국내여행",
    "hook_lines": ["후킹 예시 1", "후킹 예시 2"],
    "blog_paragraphs": ["첫 문단", "둘째 문단", "셋째 문단"],
    "video_titles": ["유튜브 제목1", "유튜브 제목2"],
    "generated_text": "..."
  }
]
```

