# Auto Pipeline

This repository contains scripts for collecting trending keywords, generating marketing hooks with OpenAI, and uploading results to Notion.

## Installation

Create a virtual environment and install the required packages using `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

Execute the pipeline locally with:

```bash
python run_pipeline.py
```

Environment variables such as `OPENAI_API_KEY` and Notion database IDs should be set via a `.env` file or your shell before running.
