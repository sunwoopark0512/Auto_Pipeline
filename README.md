# Auto Pipeline

Auto Pipeline automates collection of trending keywords, generation of marketing hooks using GPT-4, and uploading the results to Notion.  Each stage can be executed individually or orchestrated through `run_pipeline.py`.

## Required Environment Variables

The scripts read configuration from the following environment variables (usually stored in a `.env` file):

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | API key for generating hooks. |
| `NOTION_API_TOKEN` | Token for accessing the Notion API. |
| `NOTION_HOOK_DB_ID` | Notion database ID for storing generated hooks. |
| `NOTION_DB_ID` | Notion database ID for storing raw keywords (used by `scripts/notion_uploader.py`). |
| `NOTION_KPI_DB_ID` | Notion database ID for KPI statistics. |
| `KEYWORD_OUTPUT_PATH` | Path for keyword JSON output/input. Defaults to `data/keyword_output_with_cpc.json`. |
| `HOOK_OUTPUT_PATH` | Path for generated hooks JSON. Defaults to `data/generated_hooks.json`. |
| `FAILED_HOOK_PATH` | Path to save failed hook generations. Defaults to `logs/failed_hooks.json`. |
| `REPARSED_OUTPUT_PATH` | JSON file used by retry scripts. Defaults to `logs/failed_keywords_reparsed.json`. |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords. Defaults to `data/uploaded_keywords_cache.json`. |
| `FAILED_UPLOADS_PATH` | Path for failed keyword uploads. Defaults to `logs/failed_uploads.json`. |
| `UPLOAD_DELAY` | Delay (seconds) between Notion uploads. |
| `RETRY_DELAY` | Delay (seconds) between retry attempts. |
| `API_DELAY` | Delay (seconds) between OpenAI API calls. |
| `TOPIC_CHANNELS_PATH` | Location of `topic_channels.json`. Defaults to `config/topic_channels.json`. |

## Directory Layout

- **`config/`** – contains topic configuration (`topic_channels.json`).
- **`data/`** – generated keyword lists, hook JSON files and caches.
- **`logs/`** – failure details and `notion_upload.log`.

The data and log directories are created at runtime if they do not exist.

## Running the Pipeline

### Manual Execution

Scripts can be run individually in the following typical order:

1. `python keyword_auto_pipeline.py` – collects trending keywords from Google Trends and Twitter and writes them to `data/keyword_output_with_cpc.json`.
2. `python hook_generator.py` – generates marketing hooks from the collected keywords and saves them to `data/generated_hooks.json`. Failures are written to `logs/failed_hooks.json`.
3. `python notion_hook_uploader.py` – uploads the generated hooks to the Notion database. Upload logs appear in `logs/notion_upload.log` and any failed items are stored in `data/upload_failed_hooks.json`.
4. `python retry_failed_uploads.py` – retries uploads listed in `logs/failed_keywords_reparsed.json`.
5. `python retry_dashboard_notifier.py` – posts KPI summaries of the retry results to the Notion KPI database.

Additional utilities exist in the `scripts/` folder:

- `scripts/notion_uploader.py` – uploads raw keywords to a Notion database using the same environment variables as above.
- `scripts/retry_failed_uploads.py` – retries failed keyword uploads stored in `logs/failed_keywords.json` (path configurable via `FAILED_HOOK_PATH`).

### Using `run_pipeline.py`

The `run_pipeline.py` script sequentially executes the pipeline stages listed in its `PIPELINE_SEQUENCE` variable. Running

```bash
python run_pipeline.py
```

will attempt to run each script in order. Edit the sequence if you need to customize or skip steps.

---

All generated data can be found under the `data/` directory and logs are stored under `logs/`.
