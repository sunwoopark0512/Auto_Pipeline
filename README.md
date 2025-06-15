# Auto Pipeline

이 리포지토리는 키워드 데이터를 수집하고, GPT를 통해 마케팅 후킹 문장을 생성한 뒤 Notion에 업로드하는 과정을 자동화합니다. 주요 단계는 다음과 같습니다.

1. **키워드 수집** - `keyword_auto_pipeline.py`
2. **후킹 생성** - `hook_generator.py`
3. **Notion 업로드** - `notion_hook_uploader.py`
4. **실패 재시도** - `retry_failed_uploads.py` 및 `retry_dashboard_notifier.py`

## 파이프라인 흐름

```
키워드 수집 → 후킹 생성 → Notion 업로드 → 실패 재시도
```

## 환경 변수

| 환경 변수 | 설명 | 기본값 |
|-----------|------|-------|
| `OPENAI_API_KEY` | OpenAI API 키 | - |
| `NOTION_API_TOKEN` | Notion 통합 토큰 | - |
| `NOTION_HOOK_DB_ID` | 후킹 저장용 Notion DB ID | - |
| `NOTION_KPI_DB_ID` | KPI 저장용 Notion DB ID | - |
| `KEYWORD_OUTPUT_PATH` | 키워드 JSON 저장 경로 | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | 생성된 후킹 JSON 경로 | `data/generated_hooks.json` |
| `REPARSED_OUTPUT_PATH` | 재시도용 실패 로그 경로 | `logs/failed_keywords_reparsed.json` |

기타 세부 동작에 필요한 변수들은 코드 주석을 참고하세요.

## 로컬 실행 방법

1. 위 환경 변수를 `.env` 파일에 설정합니다.
2. 의존성을 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
3. 파이프라인을 실행합니다.
   ```bash
   python run_pipeline.py
   ```

## GitHub Actions 사용

`.github/workflows/daily-pipeline.yml.txt` 파일을 이용해 매일 자동으로 파이프라인을 실행할 수 있습니다. 리포지토리의 `Secrets` 설정에 위 환경 변수를 등록하면 됩니다.
