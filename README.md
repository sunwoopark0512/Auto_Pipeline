## ab_variant_manager \uc0ac\uc6a9\ubc95

```bash
export SUPABASE_URL="https://xyz.supabase.co"
export SUPABASE_ANON_KEY="public-anon-key"
export OPENAI_API_KEY="sk-..."
python ab_variant_manager.py --table content --limit 5 --title-variants 3 --thumb-variants 2
```

```mermaid
flowchart TD
    A[Fetch rows needing variants] --> B[GPT: generate title variants]
    B --> C[GPT: generate thumbnail snippets]
    C --> D[Update Supabase row<br/>with JSON arrays + ab_test_ready]
```
