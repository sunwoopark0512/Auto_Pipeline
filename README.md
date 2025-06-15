# Auto Pipeline

This repository automates the process of collecting trending keywords, generating marketing hooks with GPT, and pushing everything to Notion. Each step is orchestrated through Python scripts.

## Key Components

- [keyword_auto_pipeline.py](keyword_auto_pipeline.py): gathers keywords from Google Trends and Twitter and stores them in `data/keyword_output_with_cpc.json`.
- [scripts/notion_uploader.py](scripts/notion_uploader.py): uploads filtered keywords to a Notion database.
- [hook_generator.py](hook_generator.py): generates marketing hooks and content drafts using OpenAI based on the collected keywords.
- [notion_hook_uploader.py](notion_hook_uploader.py): uploads generated hooks and drafts to another Notion database.
- [run_pipeline.py](run_pipeline.py): executes the above scripts in sequence.

## Pipeline Overview

```mermaid
flowchart TD
    A[Keyword & Trend Collection] --> B[Keyword Upload]
    B --> C[Hook Generation]
    C --> D[Notion Hook Upload]
```

## Detailed Sequence

```mermaid
sequenceDiagram
    participant K as keyword_auto_pipeline.py
    participant U as notion_uploader.py
    participant H as hook_generator.py
    participant N as notion_hook_uploader.py
    K->>U: Save keywords & upload to Notion
    U-->>H: Provide filtered keywords
    H->>N: Produce hooks
    N->>Notion: Push pages
```

Run `python run_pipeline.py` to execute the full workflow or run individual scripts as needed.

