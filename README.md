## auto_insight 사용법

```bash
export SUPABASE_URL=... SUPABASE_ANON_KEY=...
export OPENAI_API_KEY=...
export NOTION_TOKEN="secret_xxx"
python auto_insight.py --table content --days 7 --notion-db YOUR_DB_ID
```

```mermaid
flowchart TD
    A[Pull last N-days rows<br/>from Supabase] --> B[Compute stats (pandas)]
    B --> C[GPT-4o executive summary]
    C --> D[Create Notion page<br/>with props + text]
```
