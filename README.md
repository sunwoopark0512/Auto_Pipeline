# Auto Pipeline

This repository contains automation scripts for generating marketing hooks and uploading them to Notion. The main entry point is `run_pipeline.py` which sequentially executes helper scripts.

## Installation

```bash
pip install -r requirements.txt  # install dependencies
```

Create a `.env` file with credentials:

```env
OPENAI_API_KEY=...
NOTION_API_TOKEN=...
NOTION_HOOK_DB_ID=...
NOTION_KPI_DB_ID=...
```

## Usage

Run the pipeline from the project root:

```bash
python run_pipeline.py
```

The workflow will generate hooks, upload them to Notion and update KPI dashboards. See `.github/workflows/daily-pipeline.yml.txt` for CI scheduling details.
