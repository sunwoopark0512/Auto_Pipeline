## podcast_creator 사용법

```bash
export SUPABASE_URL="https://xyz.supabase.co"
export SUPABASE_ANON_KEY="public-anon-key"
export PODCAST_RSS_FILE="podcast_feed.xml"
python podcast_creator.py --table content --limit 5
```

```mermaid
flowchart TD
    A[Fetch pending rows] --> B[Generate MP3 via gTTS]
    B --> C[Upload to Supabase Storage]
    C --> D[Append <item> to RSS file]
    D --> E[Update DB flags + URLs]
```
