# Auto Pipeline

This repository contains a set of scripts that gather trending keywords, generate marketing hooks using OpenAI, and upload the results to Notion.

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Set the following variables (e.g. in a `.env` file):

- `OPENAI_API_KEY` – API key for OpenAI.
- `NOTION_API_TOKEN` – integration token for the Notion API.
- `NOTION_HOOK_DB_ID` – ID of the Notion database used for generated hooks.
- `NOTION_DB_ID` – Notion database ID for keyword metrics (used by `scripts/notion_uploader.py`).
- `NOTION_KPI_DB_ID` – Notion database ID where retry statistics are stored.
- `KEYWORD_OUTPUT_PATH` – path for keyword data (default `data/keyword_output_with_cpc.json`).
- `HOOK_OUTPUT_PATH` – path for generated hooks (default `data/generated_hooks.json`).
- `FAILED_HOOK_PATH` – path for failed hook generation log (default `logs/failed_hooks.json`).
- `UPLOADED_CACHE_PATH` – cache file for uploaded keywords.
- `FAILED_UPLOADS_PATH` – path where failed uploads are stored.
- `REPARSED_OUTPUT_PATH` – path for parsed failed items.
- `UPLOAD_DELAY` – delay between Notion API requests.
- `API_DELAY` – delay between OpenAI API calls.
- `RETRY_DELAY` – delay between retry attempts.
- `TOPIC_CHANNELS_PATH` – path to `config/topic_channels.json`.

## Usage

1. **Collect Keywords**
   ```bash
   python keyword_auto_pipeline.py
   ```
   This creates a JSON file with filtered keywords based on Google Trends and Twitter data.

2. **Generate Hooks**
   ```bash
   python hook_generator.py
   ```
   Uses OpenAI to create hook sentences and drafts for each keyword.

3. **Upload to Notion**
   ```bash
   python notion_hook_uploader.py
   ```
   Uploads the generated hooks to your Notion database.

Optional helper scripts are available in the `scripts/` directory for uploading keyword metrics and retrying failed uploads. The `run_pipeline.py` script can be used to chain multiple steps.

## Configuration

Default topics are listed in `config/topic_channels.json`. Output and log directories (`data/` and `logs/`) will be created automatically as needed.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for details.

