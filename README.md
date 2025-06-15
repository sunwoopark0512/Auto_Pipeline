# Auto Pipeline

This repository contains a set of Python scripts for generating and uploading marketing hooks to Notion. The pipeline gathers trending keywords, creates hook texts using OpenAI, uploads them to a Notion database and retries any failed uploads.

## Requirements
Install dependencies using:
```bash
pip install -r requirements.txt
```

## Usage
Run the entire pipeline locally:
```bash
python run_pipeline.py
```
Environment variables such as `OPENAI_API_KEY`, `NOTION_API_TOKEN` and database IDs must be configured (e.g. via a `.env` file).

The GitHub Actions workflow runs the same entrypoint on a daily schedule.
