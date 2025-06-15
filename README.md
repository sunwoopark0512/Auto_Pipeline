# Auto Pipeline

이 저장소는 트렌드 키워드를 수집하고 GPT로 후킹 문구를 생성한 뒤, Notion 데이터베이스에 업로드하는 자동화 스크립트를 모아 놓았습니다. 주요 흐름은 다음과 같습니다.

1. **키워드 수집** (`keyword_auto_pipeline.py`)
   - Google Trends와 Twitter 데이터를 이용해 키워드를 추출합니다.
   - CPC 값을 부여하고 필터링하여 `KEYWORD_OUTPUT_PATH` 경로에 저장합니다.
2. **GPT 후킹 생성** (`hook_generator.py`)
   - 수집된 키워드를 바탕으로 OpenAI API를 호출해 후킹 문장과 블로그 초안, 영상 제목을 만듭니다.
   - 결과는 `HOOK_OUTPUT_PATH`에 저장하며 실패한 항목은 `FAILED_HOOK_PATH`에 기록합니다.
3. **Notion 업로드** (`notion_hook_uploader.py`)
   - 생성된 후킹 결과를 `NOTION_HOOK_DB_ID`로 지정된 데이터베이스에 업로드합니다.
   - 중복 여부를 확인하고 필요 시 재시도합니다.
4. **업로드 실패 재시도** (`retry_failed_uploads.py`)
   - `REPARSED_OUTPUT_PATH` 파일에 남은 실패 항목을 다시 업로드합니다.
5. **KPI 대시보드 갱신** (`retry_dashboard_notifier.py`)
   - 재시도 결과를 집계해 KPI 데이터베이스(`NOTION_KPI_DB_ID`)에 기록합니다.

## 주요 환경 변수

| 변수 | 설명 | 사용 스크립트 |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API 키 | `hook_generator.py` |
| `NOTION_API_TOKEN` | Notion API 토큰 | 대부분의 Notion 관련 스크립트 |
| `NOTION_HOOK_DB_ID` | 후킹 저장용 Notion DB ID | `notion_hook_uploader.py`, `retry_failed_uploads.py`, `scripts/retry_failed_uploads.py` |
| `NOTION_KPI_DB_ID` | KPI 기록용 Notion DB ID | `retry_dashboard_notifier.py` |
| `NOTION_DB_ID` | 키워드 메트릭 저장용 DB ID | `scripts/notion_uploader.py` |
| `TOPIC_CHANNELS_PATH` | 토픽 설정 파일 경로 | `keyword_auto_pipeline.py` |
| `KEYWORD_OUTPUT_PATH` | 필터링된 키워드 JSON 경로 | `keyword_auto_pipeline.py`, `hook_generator.py`, `scripts/notion_uploader.py` |
| `HOOK_OUTPUT_PATH` | GPT 결과 저장 경로 | `hook_generator.py`, `notion_hook_uploader.py` |
| `FAILED_HOOK_PATH` | 후킹 생성 실패 항목 저장 경로 | `hook_generator.py`, `scripts/retry_failed_uploads.py` |
| `REPARSED_OUTPUT_PATH` | 업로드 실패 재파싱 결과 경로 | `retry_failed_uploads.py`, `retry_dashboard_notifier.py` |
| `UPLOAD_DELAY` | Notion 업로드 간 대기 시간 | `notion_hook_uploader.py`, `scripts/notion_uploader.py` |
| `RETRY_DELAY` | 실패 재시도 간 대기 시간 | `retry_failed_uploads.py`, `scripts/retry_failed_uploads.py` |
| `API_DELAY` | OpenAI 호출 간 대기 시간 | `hook_generator.py` |
| `UPLOADED_CACHE_PATH` | 업로드 완료 키워드 캐시 | `scripts/notion_uploader.py` |
| `FAILED_UPLOADS_PATH` | 키워드 업로드 실패 기록 | `scripts/notion_uploader.py` |

## 로컬 실행 방법

1. 의존성 설치:

```bash
pip install -r requirements.txt
```

2. `.env` 파일에 필요한 API 키와 데이터베이스 ID를 설정합니다.

3. 각 단계를 순서대로 실행하거나 `run_pipeline.py` 스크립트로 한번에 실행할 수 있습니다.

```bash
python keyword_auto_pipeline.py
python hook_generator.py
python notion_hook_uploader.py
python retry_failed_uploads.py
python retry_dashboard_notifier.py
```

`run_pipeline.py`는 여러 단계를 연속으로 실행하도록 구성돼 있습니다.

## GitHub Actions 사용

`.github/workflows/daily-pipeline.yml.txt` 워크플로가 매일 파이프라인을 자동으로 실행합니다. 리포지터리 시크릿으로 환경 변수를 설정하고, 의존성을 설치한 뒤 `scripts/run_pipeline.py`를 실행합니다. 실패한 항목은 워크플로 아티팩트로 업로드되며, 실행 요약이 워크플로 대시보드에 남습니다.
