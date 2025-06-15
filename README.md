# Auto Pipeline

This project automates the generation and upload of marketing hooks to Notion.
It collects trending keywords, creates content suggestions using OpenAI, and
pushes the results to Notion databases. The scripts are designed to be run as a
sequence but can also operate individually.

## Pipeline Steps

1. **`keyword_auto_pipeline.py`** – gather trending keywords from Google Trends
   and Twitter.
2. **`hook_generator.py`** – generate hook sentences and post ideas with the
   OpenAI API using the keywords from the previous step.
3. **`notion_hook_uploader.py`** – upload generated hooks to the Notion hook
   database.
4. **`retry_failed_uploads.py`** – retry uploads that previously failed.
5. **`retry_dashboard_notifier.py`** – record KPI metrics for retries in a
   separate Notion dashboard.
6. **`run_pipeline.py`** – orchestrate the above scripts in order.

## Running the Pipeline

1. Copy `.env.example` to `.env` and provide values for every variable.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Execute all steps with:

```bash
python run_pipeline.py
```

You can also invoke each script directly if you only need part of the pipeline.

## Continuous Delivery

The workflow file `.github/workflows/daily-pipeline.yml.txt` runs this pipeline
on GitHub Actions every day or when triggered manually. It checks out the
repository, installs dependencies, and runs `python scripts/run_pipeline.py`
with the required secrets (`OPENAI_API_KEY`, `NOTION_API_TOKEN`, etc.).
