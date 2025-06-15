# Auto Pipeline

This project generates marketing hooks from trending keywords and uploads the results to Notion.

## Pipeline Overview

The main entry point is `run_pipeline.py`. It sequentially executes a set of scripts found in the `scripts/` directory:

1. `hook_generator.py` – generate hook copy with OpenAI.
2. `parse_failed_gpt.py` – parse failed GPT outputs and save them to `logs/failed_keywords_reparsed.json`.
3. `retry_failed_uploads.py` – upload items that previously failed to Notion.
4. `notify_retry_result.py` – send a Slack message summarising retry results.
5. `retry_dashboard_notifier.py` – push KPI information to a Notion dashboard.

Configure environment variables in a `.env` file before running the pipeline:

```bash
python run_pipeline.py
```

Each script logs its own progress to the console and may create files inside the `logs/` directory.
