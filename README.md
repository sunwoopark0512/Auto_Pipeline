# Auto Pipeline

This repository contains small utilities for generating marketing hooks and uploading them to Notion. All scripts rely on environment variables loaded via `.env`.

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI | |
| `NOTION_API_TOKEN` | Token for Notion API | |
| `NOTION_HOOK_DB_ID` | Notion database ID for generated hooks | |
| `NOTION_KPI_DB_ID` | Notion database ID used for KPI logging | |
| `NOTION_DB_ID` | Notion database ID for keyword uploads | |
| `TOPIC_CHANNELS_PATH` | Path to topic configuration JSON | `config/topic_channels.json` |
| `KEYWORD_OUTPUT_PATH` | Output path for keyword collection | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | Output path for generated hooks | `data/generated_hooks.json` |
| `FAILED_HOOK_PATH` | Location of failed hook items and reparsed data | `logs/failed_keywords_reparsed.json` |
| `FAILED_UPLOADS_PATH` | Location of failed upload logs | `logs/failed_uploads.json` |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords | `data/uploaded_keywords_cache.json` |
| `UPLOAD_DELAY` | Delay between Notion uploads (seconds) | `0.5` |
| `RETRY_DELAY` | Delay between retry attempts (seconds) | `0.5` |
| `API_DELAY` | Delay between OpenAI API calls (seconds) | `1.0` |

Create a `.env` file based on the `.env.template` provided and fill in the required credentials.

## Usage

Run individual scripts with Python. For example, to upload generated hooks:

```bash
python notion_hook_uploader.py
```

A GitHub Actions workflow is available at `.github/workflows/daily-pipeline.yml.txt` for automated execution.

