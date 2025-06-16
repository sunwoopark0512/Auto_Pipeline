# Auto Pipeline

This repository contains a set of scripts to build keyword lists, generate marketing hooks with OpenAI, and upload the results to Notion. The pipeline can run manually or on a schedule through GitHub Actions.

## Installation

1. Install Python 3.10 or later.
2. Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root containing the environment variables below. Secrets can also be provided through GitHub repository secrets when running via Actions.

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | API key for calling OpenAI to generate hooks. |
| `NOTION_API_TOKEN` | Token for the Notion integration. |
| `NOTION_DB_ID` | Database ID for storing raw keywords. Used by `scripts/notion_uploader.py`. |
| `NOTION_HOOK_DB_ID` | Database ID where generated hooks are uploaded. |
| `NOTION_KPI_DB_ID` | Database for storing retry statistics. |
| `KEYWORD_OUTPUT_PATH` | Path to save keyword JSON (`keyword_auto_pipeline.py`). Default `data/keyword_output_with_cpc.json`. |
| `HOOK_OUTPUT_PATH` | Path to save generated hooks (`hook_generator.py`). Default `data/generated_hooks.json`. |
| `FAILED_HOOK_PATH` | Location to store hooks that failed generation. |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords. |
| `FAILED_UPLOADS_PATH` | Log of keywords that failed to upload. |
| `REPARSED_OUTPUT_PATH` | Failed hooks that were parsed again for retry. |
| `UPLOAD_DELAY` | Delay in seconds between Notion uploads. |
| `RETRY_DELAY` | Delay in seconds for retry scripts. |
| `API_DELAY` | Delay between OpenAI API calls. |

Only the variables required by the scripts you intend to run must be set. The defaults stored in each script can be used for local testing.

## Running the Pipeline Manually

The typical end‑to‑end flow is:

```bash
python keyword_auto_pipeline.py      # fetch trending keywords
python hook_generator.py             # generate marketing hooks with GPT
python notion_hook_uploader.py       # upload hooks to Notion
python retry_failed_uploads.py       # retry any failed uploads
python retry_dashboard_notifier.py   # push retry summary to KPI database
```

To execute every step in order you can run:

```bash
python run_pipeline.py
```

Each script logs progress to the console and writes JSON files into the `data/` or `logs/` folders.

## Running with GitHub Actions

A workflow file is provided under `.github/workflows/daily-pipeline.yml.txt`. The job installs Python 3.10, installs the requirements, and then runs `python scripts/run_pipeline.py`. Secrets such as `OPENAI_API_KEY` and `NOTION_API_TOKEN` must be added to the repository settings. The workflow can be triggered on a schedule or manually using the **workflow_dispatch** event.

## Script Overview

- **keyword_auto_pipeline.py** – Collects trending keywords from Google Trends and Twitter. Results are stored in `KEYWORD_OUTPUT_PATH`. Example output snippet:

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "filtered_keywords": [
    {"keyword": "여행 국내여행", "source": "GoogleTrends", "score": 80, "growth": 1.5, "cpc": 1200}
  ]
}
```

- **hook_generator.py** – Uses OpenAI to produce two hook phrases, a short blog draft and example video titles for each keyword. Generates `HOOK_OUTPUT_PATH` and logs failed items.
- **notion_hook_uploader.py** – Uploads generated hooks to a Notion database. Example log message:

```
✅ 업로드 완료: 여행 국내여행
```

- **retry_failed_uploads.py** – Attempts to re‑upload items recorded in `REPARSED_OUTPUT_PATH` and updates the file with any remaining failures.
- **retry_dashboard_notifier.py** – Summarises retry results and writes a KPI record into another Notion database.
- **run_pipeline.py** – Convenience wrapper that runs the above scripts in order.
- **scripts/notion_uploader.py** – (optional) Uploads raw keyword metrics to a separate Notion database.
- **scripts/retry_failed_uploads.py** – Retry script for the raw keyword uploader.

Each program emits informative log statements, allowing you to monitor progress and see counts of successes or failures.

## Example Output Locations

- Generated keywords: `data/keyword_output_with_cpc.json`
- Hooks produced by GPT: `data/generated_hooks.json`
- Failed uploads to retry: `logs/failed_keywords_reparsed.json`

These files are created automatically the first time the scripts run.

