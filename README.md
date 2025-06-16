# Auto Pipeline

This project orchestrates several scripts that gather trending keywords, analyze channel ROI, generate content hooks, and upload them to Notion.

## Pipeline Steps

1. **keyword_auto_pipeline.py** – Collects trending keyword data.
2. **channel_roi_analyzer.py** – Analyzes return on investment for each channel using the collected data.
3. **hook_generator.py** – Generates hook text for the keywords.
4. **notion_hook_uploader.py** – Uploads generated hooks to the Notion database.
5. **retry_failed_uploads.py** – Retries any failed Notion uploads.
6. **retry_dashboard_notifier.py** – Updates the KPI dashboard in Notion with retry statistics.

Run the entire pipeline with:

```bash
python run_pipeline.py
```
