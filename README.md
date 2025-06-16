# Auto Pipeline

This repository automates the generation of marketing hooks from trending keywords and uploads the results to Notion.

## Installation
1. **Clone** the repository and create a Python 3.10 environment.
2. Install dependencies:
   ```bash
   pip install openai python-dotenv notion-client pytrends snscrape
   ```
   (or install from `requirements.txt` if available.)

## Required Environment Variables
The following variables must be provided (e.g. in a `.env` file or CI secrets):

- `OPENAI_API_KEY` – API key for OpenAI
- `NOTION_API_TOKEN` – Notion integration token
- `NOTION_DB_ID` – Database ID for uploading raw keywords (`scripts/notion_uploader.py`)
- `NOTION_HOOK_DB_ID` – Database ID for generated hooks
- `NOTION_KPI_DB_ID` – Database ID for retry KPI statistics
- `SLACK_WEBHOOK_URL` – Slack webhook for workflow notifications
- Optional variables controlling paths and delays:
  - `TOPIC_CHANNELS_PATH` (default `config/topic_channels.json`)
  - `KEYWORD_OUTPUT_PATH` (default `data/keyword_output_with_cpc.json`)
  - `HOOK_OUTPUT_PATH` (default `data/generated_hooks.json`)
  - `FAILED_HOOK_PATH`/`REPARSED_OUTPUT_PATH` (default under `logs/`)
  - `UPLOAD_DELAY`, `API_DELAY`, `RETRY_DELAY`

## Running the Pipeline Manually
1. Generate and filter keywords:
   ```bash
   python keyword_auto_pipeline.py
   ```
2. Create hook texts with GPT:
   ```bash
   python hook_generator.py
   ```
3. Upload results to Notion:
   ```bash
   python notion_hook_uploader.py
   ```
4. If some uploads fail, retry them:
   ```bash
   python retry_failed_uploads.py
   python retry_dashboard_notifier.py
   ```
5. Alternatively run everything in sequence with:
   ```bash
   python run_pipeline.py
   ```

### Example Output
After running `hook_generator.py` you will see logs similar to:
```text
✅ 생성 완료: 여행 국내여행
🎉 후킹 문장 저장 완료: data/generated_hooks.json
```
If an upload succeeds the log shows:
```text
✅ 업로드 완료: 여행 국내여행
```

## Running via GitHub Actions
The workflow `.github/workflows/daily-pipeline.yml.txt` triggers the pipeline daily and can be run manually through the Actions tab. Repository secrets must contain the same environment variables listed above. The workflow installs dependencies and executes `scripts/run_pipeline.py` (which invokes the pipeline scripts) and uploads logs of failed keywords.

## Script Overview
- `keyword_auto_pipeline.py` – Collects trending keywords from Google Trends and Twitter and saves filtered results to JSON.
- `hook_generator.py` – Uses GPT to generate hook sentences, blog paragraphs and video titles for each keyword.
- `notion_hook_uploader.py` – Uploads generated hooks to a Notion database.
- `retry_failed_uploads.py` – Attempts to re-upload previously failed items stored under `logs/`.
- `retry_dashboard_notifier.py` – Sends retry statistics to a KPI dashboard in Notion.
- `run_pipeline.py` – Helper that sequentially runs the scripts above.
- `scripts/notion_uploader.py` – Uploads raw keyword metrics to Notion.
- `scripts/retry_failed_uploads.py` – Legacy retry script for earlier outputs.

Example output files are written under the `data/` and `logs/` directories, such as `data/generated_hooks.json` containing generated content for each keyword.
