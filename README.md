# cursor_chunk_doc_gen

Codex / Cursor 한 파일용 **자동 Docstring 생성기**.

```bash
export OPENAI_API_KEY="sk-..."
python cursor_chunk_doc_gen.py my_script.py
Flow
mermaid
flowchart TD
    A[Load source] --> B[Parse with ast]
    B --> C{Docstring exists?}
    C -- No --> D[Prompt GPT-4o for docstring]
    D --> E[Insert docstring into AST]
    C -- Yes --> E
    E --> F[Unparse → source]
    F --> G[Write *_docgen.py]
```

---

### 📌 사용 방법 요약

```bash
# 1) 의존 설치
pip install -r requirements.txt

# 2) 실행
export OPENAI_API_KEY="YOUR_API_KEY"
python cursor_chunk_doc_gen.py your_module.py
```
