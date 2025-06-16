# Auto Pipeline

This repository contains scripts for generating and uploading content to Notion.

## Setup

1. Create a Python virtual environment (optional but recommended).
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment variables in a `.env` file as expected by the scripts (see the code for variable names).

## Usage

Run the pipeline using:

```bash
python run_pipeline.py
```

This will execute the scripts in sequence as defined in `run_pipeline.py`.
