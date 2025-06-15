# Usage

After completing the setup, you can run the entire pipeline with:

```bash
python run_pipeline.py
```

This executes the following steps:
1. Generate hooks using OpenAI (`hook_generator.py`).
2. Upload generated hooks to Notion (`notion_hook_uploader.py`).
3. Retry failed uploads and notify dashboards.

Individual scripts in `scripts/` can also be executed separately for debugging or manual control.
