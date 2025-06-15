# Auto Pipeline

This repository contains a collection of scripts for generating marketing keywords, creating hook text via OpenAI GPT, and uploading the results to Notion databases.  
Scripts are primarily in Korean and orchestrated through `run_pipeline.py`.

## Setup

1. Create a Python 3 virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and configure the environment variables described below.

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI used by `hook_generator.py`. | – |
| `NOTION_API_TOKEN` | Notion integration token. Required by upload and retry scripts. | – |
| `NOTION_DB_ID` | Database ID for uploading raw keywords (used by `scripts/notion_uploader.py`). | – |
| `NOTION_HOOK_DB_ID` | Database ID for storing generated hooks. | – |
| `NOTION_KPI_DB_ID` | Database ID for KPI metrics (`retry_dashboard_notifier.py`). | – |
| `KEYWORD_OUTPUT_PATH` | Path where keyword extraction results are saved. | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | Path where generated hooks are saved. | `data/generated_hooks.json` |
| `FAILED_HOOK_PATH` | Path to store hooks that failed to generate. | `logs/failed_hooks.json` |
| `REPARSED_OUTPUT_PATH` | Path for reparsed data used in retry scripts. | `logs/failed_keywords_reparsed.json` |
| `UPLOADED_CACHE_PATH` | Cache file for already uploaded keywords. | `data/uploaded_keywords_cache.json` |
| `FAILED_UPLOADS_PATH` | Log file for failed keyword uploads. | `logs/failed_uploads.json` |
| `API_DELAY` | Delay between OpenAI API calls. | `1.0` |
| `UPLOAD_DELAY` | Delay between Notion uploads. | `0.5` |
| `RETRY_DELAY` | Delay between retry attempts. | `0.5` |
| `TOPIC_CHANNELS_PATH` | Location of topic configuration JSON. | `config/topic_channels.json` |

## Usage

The pipeline can be run step by step or through the orchestrator script:

```bash
python run_pipeline.py
```

`run_pipeline.py` expects the scripts listed in `PIPELINE_SEQUENCE` to exist under the `scripts/` directory. Each script performs part of the workflow such as generating hooks, parsing failures and retrying uploads.

Individual scripts can be executed directly as well, for example:

```bash
python keyword_auto_pipeline.py      # gather trending keywords
python hook_generator.py             # create marketing hook text via GPT
python notion_hook_uploader.py       # upload generated hooks to Notion
```

Ensure the necessary environment variables are configured before running any script.

## Data

Output files are stored under the `data/` directory and logs under `logs/`. These paths can be customised through the environment variables above.

