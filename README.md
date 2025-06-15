# Auto Pipeline

This repository contains automation scripts for generating content and pushing results to Notion.

## Structure

- `run_pipeline.py` – orchestrates execution of individual scripts located in `scripts/`.
- `scripts/` – contains all executable pipeline stages such as `hook_generator.py` and retry helpers.

## Usage

Run the full pipeline locally:

```bash
python run_pipeline.py
```

The GitHub Actions workflow `.github/workflows/daily-pipeline.yml.txt` runs the same command on a schedule.
