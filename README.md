# Auto Pipeline

This repository contains scripts to generate marketing hooks, upload them to Notion and retry failed uploads. The pipeline relies on several environment variables.

## Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI GPT | - |
| `TOPIC_CHANNELS_PATH` | Path to topic/channel config JSON | `config/topic_channels.json` |
| `KEYWORD_OUTPUT_PATH` | Output path for generated keywords | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | Output path for generated hooks | `data/generated_hooks.json` |
| `FAILED_HOOK_PATH` | JSON file for failed hook generation logs | `logs/failed_hooks.json` |
| `REPARSED_OUTPUT_PATH` | JSON file for failed upload entries | `logs/failed_uploads.json` |
| `NOTION_API_TOKEN` | Token for Notion API | - |
| `NOTION_DB_ID` | Notion database ID for keyword upload | - |
| `NOTION_HOOK_DB_ID` | Notion database ID for hook upload | - |
| `NOTION_KPI_DB_ID` | Notion database ID for KPI logging | - |
| `UPLOAD_DELAY` | Delay between Notion uploads | `0.5` |
| `RETRY_DELAY` | Delay between retry attempts | `0.5` |
| `UPLOADED_CACHE_PATH` | Cache path for already uploaded keywords | `data/uploaded_keywords_cache.json` |
| `API_DELAY` | Delay between GPT requests | `1.0` |
