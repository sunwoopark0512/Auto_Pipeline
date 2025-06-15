# Auto Pipeline

This repository contains a set of Python scripts to collect trending keywords, generate marketing hooks using OpenAI, and upload the results to Notion databases. The main workflow can be executed through `run_pipeline.py`, which runs each step sequentially.

## Installation

1. Install Python 3.8 or higher.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with the following keys:

```
OPENAI_API_KEY=<your OpenAI API key>
NOTION_API_TOKEN=<your Notion integration token>
NOTION_DB_ID=<Notion database ID for collected keywords>
NOTION_HOOK_DB_ID=<Notion database ID for generated hooks>
NOTION_KPI_DB_ID=<Notion database ID for KPI dashboards>
# Optional paths and tuning parameters
KEYWORD_OUTPUT_PATH=data/keyword_output_with_cpc.json
HOOK_OUTPUT_PATH=data/generated_hooks.json
FAILED_HOOK_PATH=logs/failed_hooks.json
REPARSED_OUTPUT_PATH=logs/failed_keywords_reparsed.json
UPLOADED_CACHE_PATH=data/uploaded_keywords_cache.json
FAILED_UPLOADS_PATH=logs/failed_uploads.json
UPLOAD_DELAY=0.5
RETRY_DELAY=0.5
API_DELAY=1.0
TOPIC_CHANNELS_PATH=config/topic_channels.json
```

Adjust the paths and delay values as needed for your environment.

## Usage

Run the entire pipeline:

```bash
python run_pipeline.py
```

You can also execute individual steps manually:

```bash
python keyword_auto_pipeline.py      # Collect trending keywords
python hook_generator.py             # Generate hook sentences using GPT
python notion_hook_uploader.py       # Upload generated hooks to Notion
python retry_failed_uploads.py       # Retry any failed uploads
python retry_dashboard_notifier.py   # Push KPI metrics to Notion
```

The pipeline outputs data in the `data/` directory and logs under `logs/`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
