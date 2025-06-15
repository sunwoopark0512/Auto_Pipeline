# Auto Pipeline

This repository contains automation scripts for content generation and publishing pipelines.

## auto_rewriter 사용법

```bash
export SUPABASE_URL="https://xyz.supabase.co"
export SUPABASE_ANON_KEY="public-anon-key"
export OPENAI_API_KEY="sk-..."
python auto_rewriter.py --table content --threshold 0.25
```

```mermaid
flowchart TD
    A[Query low KPI rows] --> B[GPT-4o rewrite]
    B --> C[Update Supabase row\n+ needs_rewrite=true]
    C --> D[Downstream publisher\n(CI 또는 cron)]
```

### ✔️ 실행 빠른 체크리스트

1. **의존 설치**  
   `pip install -r requirements.txt`
2. **환경 변수**  
   `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `OPENAI_API_KEY`
3. **테스트 실행**  
   `pytest -q`
4. **실전 실행**  
   `python auto_rewriter.py --table content --threshold 0.25`
