# Auto Pipeline

This repository contains Python scripts that collect trending keywords, generate marketing hooks using GPT, and upload results to Notion databases. The scripts are designed to run individually or as a single pipeline.

## Setup

1. Ensure Python 3.10 or later is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and define the environment variables listed below.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key used by `hook_generator.py` for OpenAI requests. |
| `NOTION_API_TOKEN` | Notion integration token for all upload scripts. |
| `NOTION_DB_ID` | Database ID used by `scripts/notion_uploader.py` to store keyword metrics. |
| `NOTION_HOOK_DB_ID` | Database ID used for uploading generated hooks. |
| `NOTION_KPI_DB_ID` | Database ID for retry statistics in `retry_dashboard_notifier.py`. |
| `KEYWORD_OUTPUT_PATH` | Output file for collected keyword metrics (default `data/keyword_output_with_cpc.json`). |
| `HOOK_OUTPUT_PATH` | Output file for generated hooks (default `data/generated_hooks.json`). |
| `FAILED_HOOK_PATH` | File used to store failed hook generations (default `logs/failed_hooks.json`). |
| `REPARSED_OUTPUT_PATH` | File containing items to retry uploading (default `logs/failed_keywords_reparsed.json`). |
| `UPLOAD_DELAY` | Delay between Notion uploads in seconds (default `0.5`). |
| `API_DELAY` | Delay between OpenAI API requests in seconds (default `1.0`). |
| `RETRY_DELAY` | Delay between retry attempts when uploading (default `0.5`). |
| `TOPIC_CHANNELS_PATH` | Path to topic/channel configuration (default `config/topic_channels.json`). |
| `UPLOADED_CACHE_PATH` | Cache for successfully uploaded keywords (default `data/uploaded_keywords_cache.json`). |
| `FAILED_UPLOADS_PATH` | Log file for failed keyword uploads (default `logs/failed_uploads.json`). |

## Usage

Run scripts individually as needed or execute the entire workflow using `run_pipeline.py`.

### Generate keyword metrics

```bash
python keyword_auto_pipeline.py
```

### Generate hooks with GPT

```bash
python hook_generator.py
```

### Upload hooks to Notion

```bash
python notion_hook_uploader.py
```

### Retry failed uploads

```bash
python retry_failed_uploads.py
```

### Run the full pipeline

```bash
python run_pipeline.py
```

Configuration for topics is stored in `config/topic_channels.json`. Generated data and logs are written under the `data/` and `logs/` directories.

