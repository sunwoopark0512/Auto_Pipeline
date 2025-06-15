# Auto Pipeline

This project automates the process of gathering trending keywords, generating marketing hooks with OpenAI and storing the results in Notion. Each step of the workflow is provided as a script and `run_pipeline.py` ties them together.

## Pipeline Flow

1. **Keyword collection** (`keyword_auto_pipeline.py`)
   - Fetches trending data from Google Trends and Twitter.
   - Filters keywords based on metrics such as score, growth and mentions.
   - Outputs a JSON file (default: `data/keyword_output_with_cpc.json`).
2. **Hook generation** (`hook_generator.py`)
   - Uses the collected keywords to request GPT and generate hook sentences, blog drafts and video titles.
   - Saves the result to `data/generated_hooks.json`.
3. **Upload to Notion** (`notion_hook_uploader.py`)
   - Creates pages in a Notion database using the generated hooks.
4. **Retry failed uploads** (`retry_failed_uploads.py`)
   - Retries creating Notion pages for any items that failed in the previous step.
5. **Dashboard update** (`retry_dashboard_notifier.py`)
   - Summarises retry results and pushes KPI information to a separate Notion database.
6. **Automation runner** (`run_pipeline.py`)
   - Executes the above scripts in sequence. You can modify `PIPELINE_SEQUENCE` in `run_pipeline.py` to adjust the order or included steps.

## Setup

1. Clone the repository and create a virtual environment if desired.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your credentials and options. Important variables include:
   - `OPENAI_API_KEY` – OpenAI API token
   - `NOTION_API_TOKEN` – Notion integration token
   - `NOTION_DB_ID` – Notion database ID for keyword uploads
   - `NOTION_HOOK_DB_ID` – Notion database ID for generated hooks
   - `NOTION_KPI_DB_ID` – Notion database ID for KPI/dashboards
   - Paths such as `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH` etc. (defaults are already set)

## Running the Pipeline

After configuring the environment variables, run the pipeline from the project root:

```bash
python run_pipeline.py
```

Each step prints progress information to the console. Logs and intermediate JSON files are written under the `logs/` and `data/` directories.

