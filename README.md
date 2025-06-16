# Auto Pipeline

이 저장소는 키워드 수집부터 Notion 업로드까지의 전체 작업을 자동화하는 스크립트 모음입니다. 각 스크립트는 독립적으로 실행할 수 있으며 `run_pipeline.py`를 통해 일련의 과정을 순차적으로 실행할 수도 있습니다.

## 설치

1. Python 3.10 이상이 필요합니다.
2. 의존성 설치:

```bash
pip install -r requirements.txt
```

3. 프로젝트 루트에 `.env` 파일을 생성하여 필요한 토큰과 설정 값을 등록합니다. 아래 환경 변수 목록을 참고하세요.

## 스크립트 개요 및 환경 변수

### `keyword_auto_pipeline.py`
- **목적**: Google Trends와 Twitter에서 키워드를 수집하고 필터링합니다.
- **환경 변수**
  - `TOPIC_CHANNELS_PATH` : 토픽 목록(JSON) 경로. 기본값 `config/topic_channels.json`
  - `KEYWORD_OUTPUT_PATH` : 결과 저장 경로. 기본값 `data/keyword_output_with_cpc.json`
- **실행 예시**
  ```bash
  python keyword_auto_pipeline.py
  ```

### `hook_generator.py`
- **목적**: 키워드를 기반으로 OpenAI API를 사용해 마케팅 후킹 문장을 생성합니다.
- **환경 변수**
  - `KEYWORD_OUTPUT_PATH` : 키워드 입력 파일 경로
  - `HOOK_OUTPUT_PATH` : 생성 결과 저장 경로. 기본값 `data/generated_hooks.json`
  - `FAILED_HOOK_PATH` : 실패 항목 저장 경로. 기본값 `logs/failed_hooks.json`
  - `OPENAI_API_KEY` : OpenAI API 키
  - `API_DELAY` : API 호출 간 대기 시간(초). 기본값 `1.0`
- **실행 예시**
  ```bash
  python hook_generator.py
  ```

### `notion_hook_uploader.py`
- **목적**: 생성된 후킹 문장을 Notion 데이터베이스에 업로드합니다.
- **환경 변수**
  - `NOTION_API_TOKEN` : Notion 통합 토큰
  - `NOTION_HOOK_DB_ID` : 업로드할 데이터베이스 ID
  - `HOOK_OUTPUT_PATH` : 입력 JSON 경로. 기본값 `data/generated_hooks.json`
  - `UPLOAD_DELAY` : 업로드 간 대기 시간(초). 기본값 `0.5`
- **실행 예시**
  ```bash
  python notion_hook_uploader.py
  ```

### `scripts/notion_uploader.py`
- **목적**: 필터링된 키워드를 Notion으로 전송합니다.
- **환경 변수**
  - `NOTION_API_TOKEN` : Notion 통합 토큰
  - `NOTION_DB_ID` : 데이터베이스 ID
  - `KEYWORD_OUTPUT_PATH` : 키워드 JSON 경로
  - `UPLOAD_DELAY` : 업로드 간 대기 시간. 기본값 `0.5`
  - `UPLOADED_CACHE_PATH` : 업로드 캐시 파일 경로. 기본값 `data/uploaded_keywords_cache.json`
  - `FAILED_UPLOADS_PATH` : 실패 항목 저장 경로. 기본값 `logs/failed_uploads.json`

### `scripts/retry_failed_uploads.py`
- **목적**: 업로드에 실패한 항목을 다시 Notion으로 전송합니다.
- **환경 변수**
  - `NOTION_API_TOKEN`
  - `NOTION_HOOK_DB_ID`
  - `FAILED_HOOK_PATH` : 실패 항목 JSON 경로. 기본값 `logs/failed_keywords.json`
  - `RETRY_DELAY` : 재시도 간 대기 시간. 기본값 `0.5`

### `retry_failed_uploads.py`
- **목적**: 재파싱된 후킹 데이터를 다시 업로드합니다.
- **환경 변수**
  - `NOTION_API_TOKEN`
  - `NOTION_HOOK_DB_ID`
  - `REPARSED_OUTPUT_PATH` : 재파싱 JSON 경로. 기본값 `logs/failed_keywords_reparsed.json`
  - `RETRY_DELAY` : 재시도 간 대기 시간. 기본값 `0.5`

### `retry_dashboard_notifier.py`
- **목적**: 재시도 결과를 요약하여 Notion KPI 대시보드에 기록합니다.
- **환경 변수**
  - `NOTION_API_TOKEN`
  - `NOTION_KPI_DB_ID`
  - `REPARSED_OUTPUT_PATH` : 재시도 결과 JSON 경로

### `run_pipeline.py`
- **목적**: 위 스크립트들을 순차적으로 실행하는 간단한 파이프라인 실행기입니다.
- **실행 예시**
  ```bash
  python run_pipeline.py
  ```

## GitHub Actions

`.github/workflows/daily-pipeline.yml.txt` 파일을 `.yml` 확장자로 변경해 사용하면 매일 정해진 시간에 파이프라인을 자동으로 실행할 수 있습니다. 필요 토큰은 GitHub 저장소의 **Secrets**에 등록해야 하며, workflow 파일의 `env` 항목을 참고해 설정합니다.

## 실행 순서 예시

1. `keyword_auto_pipeline.py`로 키워드 수집
2. `hook_generator.py`로 후킹 문장 생성
3. `notion_hook_uploader.py` 또는 `scripts/notion_uploader.py`로 Notion 업로드
4. 실패 항목이 있을 경우 `scripts/retry_failed_uploads.py` 또는 `retry_failed_uploads.py` 실행
5. `retry_dashboard_notifier.py`로 KPI 업데이트

모든 과정을 한 번에 수행하려면 `run_pipeline.py`를 실행하세요.

