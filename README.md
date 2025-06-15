# Auto Pipeline

This project contains utilities for generating and uploading content to Notion.

## Retrying failed uploads

If an upload step fails, items are stored in `logs/failed_keywords_reparsed.json`.
Run the retry script from the repository root:

```bash
python retry_failed_uploads.py
```

This script used to live in `scripts/`, but now resides at the root of the
repository.
