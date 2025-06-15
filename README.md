# Auto Pipeline

This repository contains scripts that automate generation and upload of Notion hooks.

## Running the pipeline

`run_pipeline.py` sequentially executes a set of scripts. Each script can live either in the
project root or under the `scripts/` directory. The current sequence is:

1. `hook_generator.py` – generates hook sentences using OpenAI API.
2. `retry_failed_uploads.py` – retries Notion uploads that previously failed.
3. `retry_dashboard_notifier.py` – pushes aggregated retry statistics to Notion.

Run the pipeline with:

```bash
python run_pipeline.py
```

Environment variables such as API keys and Notion database IDs should be provided for each
script to work correctly.
