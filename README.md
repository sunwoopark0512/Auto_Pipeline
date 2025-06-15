# Auto Pipeline

Utilities to generate marketing hooks and upload them to Notion.

## Setup
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Create a `.env` file based on `.env.example` and fill in your credentials.

## Environment Variables
See `.env.example` for a full list. Key paths include:
- `FAILED_HOOKS_PATH` : file to store hooks that failed to generate.
- `RETRY_ITEMS_PATH`  : file used for retry uploads after parsing failures.

## Running
Execute individual scripts or run the pipeline:
```bash
python run_pipeline.py
```
