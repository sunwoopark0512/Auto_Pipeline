## hook_uploader 사용법

```bash
export SUPABASE_URL=...
export SUPABASE_ANON_KEY=...
export YT_CREDENTIALS_FILE=yt_credentials.json
export MEDIUM_TOKEN=...
export X_BEARER_TOKEN=...
export OPENAI_API_KEY=...
python hook_uploader.py --table content --limit 10
```

Flow
```mermaid
flowchart TD
    A[Supabase rows<br/>publish_ready & !published] --> B[Pick highest-priority channel]
    B --> C[Uploader plugin<br/>(YouTube·Medium·X·Tistory)]
    C --> D[Upload & get public URL]
    D --> E[Update Supabase row<br/>published=true]
```
