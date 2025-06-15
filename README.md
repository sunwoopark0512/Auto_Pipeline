# Auto Pipeline

This repository contains scripts for generating marketing hooks and uploading results to Notion.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in the required values.
   ```bash
   cp .env.example .env
   ```

The environment variables include your OpenAI key and Notion tokens as well as optional paths and delays used by the scripts.

## Running

Execute the pipeline via:
```bash
python run_pipeline.py
```

Individual scripts can also be run directly from the `scripts/` directory.

