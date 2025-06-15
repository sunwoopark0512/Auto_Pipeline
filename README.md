# Auto Pipeline

This repository contains automation scripts for generating marketing hooks and uploading them to Notion.

## Pipeline Overview

The main entrypoint is `run_pipeline.py`. It runs a set of scripts in order:

1. `hook_generator.py` – generate hook content using GPT and save the results.
2. `retry_failed_uploads.py` – retry uploads for items that previously failed.
3. `retry_dashboard_notifier.py` – push retry KPI data to the Notion dashboard.

The pipeline will log progress for each step and continue even if a script fails.

## GitHub Workflow

The `Daily Notion Hook Pipeline` workflow in `.github/workflows/daily-pipeline.yml.txt` executes `python run_pipeline.py` on a schedule. Failed items are uploaded as artifacts for review.

