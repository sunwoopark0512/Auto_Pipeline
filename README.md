# Auto Pipeline

This project automates the generation of marketing hooks and the upload of results to Notion. The pipeline is composed of several scripts which can be run locally or scheduled via GitHub Actions.

## Setup

1. **Clone the repository** and install the required Python packages. A typical setup uses `requirements.txt`:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. **Create a `.env` file** in the project root and provide the credentials described below.
3. Optionally adjust any of the configurable paths or delays via environment variables.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key used by `hook_generator.py` | - |
| `NOTION_API_TOKEN` | Token for accessing Notion API | - |
| `NOTION_DB_ID` | Database ID for raw keyword uploads (`scripts/notion_uploader.py`) | - |
| `NOTION_HOOK_DB_ID` | Database ID for generated hooks (`notion_hook_uploader.py`) | - |
| `NOTION_KPI_DB_ID` | Database ID for KPI dashboard (`retry_dashboard_notifier.py`) | - |
| `TOPIC_CHANNELS_PATH` | Path to topic configuration | `config/topic_channels.json` |
| `KEYWORD_OUTPUT_PATH` | Path to save keyword results | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | Path to save generated hook data | `data/generated_hooks.json` |
| `FAILED_HOOK_PATH` | File to store failed hook generations | `logs/failed_hooks.json` |
| `UPLOADED_CACHE_PATH` | Cache file for uploaded keywords | `data/uploaded_keywords_cache.json` |
| `FAILED_UPLOADS_PATH` | File to store failed keyword uploads | `logs/failed_uploads.json` |
| `REPARSED_OUTPUT_PATH` | File containing failed keywords for retry | `logs/failed_keywords_reparsed.json` |
| `UPLOAD_DELAY` | Sleep time between Notion uploads | `0.5` |
| `API_DELAY` | Delay between OpenAI API calls | `1.0` |
| `RETRY_DELAY` | Delay between retry attempts | `0.5` |

Values can be exported in your shell or placed inside `.env` which is loaded by most scripts.

## Running the Pipeline Manually

Execute the full workflow using the main entrypoint:

```bash
python run_pipeline.py
```

Each step prints progress information. A successful run shows messages like:

```
2023-01-01 09:00:00 INFO:🚀 실행 중: hook_generator.py
2023-01-01 09:00:10 INFO:✅ 완료: hook_generator.py
```

## Running with GitHub Actions

A workflow file is provided in `.github/workflows/daily-pipeline.yml.txt`. When configured in your repository and renamed with a `.yml` extension, it schedules the pipeline to run daily:

```yaml
- name: ▶️ Run full pipeline (single entrypoint)
  run: python scripts/run_pipeline.py
```

Secrets defined in your GitHub repository should supply the environment variables listed above.

## Script Overview

| Script | Purpose | Example Output |
|-------|---------|---------------|
| `keyword_auto_pipeline.py` | Collect trending keywords from Google Trends and Twitter and save filtered results. | `필터링된 키워드 개수: 5` |
| `hook_generator.py` | Use OpenAI to generate marketing hooks and blog/video ideas for each keyword. | `✅ 생성 완료: 여행 국내여행` |
| `notion_hook_uploader.py` | Upload generated hooks into a Notion database. | `📊 후킹 업로드 요약` |
| `retry_failed_uploads.py` | Retry uploading hooks that previously failed. | `📦 재시도 업로드 요약` |
| `retry_dashboard_notifier.py` | Push KPI statistics about retries to a Notion dashboard. | `📊 Notion KPI 업데이트 완료` |
| `scripts/notion_uploader.py` | Upload raw keyword metrics to a separate Notion database. | `📦 업로드 캐시 저장 완료: data/uploaded_keywords_cache.json` |
| `scripts/retry_failed_uploads.py` | Retry keyword uploads that failed when using `notion_uploader.py`. | `성공: 3 | 실패 유지: 1` |
| `run_pipeline.py` | Orchestrate all scripts in sequence. | `🎯 파이프라인 전체 완료` |

The log snippets above mirror lines found in the source code and help new contributors know what to expect when running each component.

