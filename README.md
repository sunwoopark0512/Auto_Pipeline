# Auto Pipeline

This repository contains scripts for generating marketing hooks and uploading them to Notion. The workflow relies on a set of Python scripts orchestrated via `run_pipeline.py` or GitHub Actions.

## Installation

Create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Most scripts rely on environment variables provided via a `.env` file. After configuring the required keys, you can run the full pipeline:

```bash
python run_pipeline.py
```

Individual scripts can also be executed directly if needed.


