# Auto Pipeline

이 저장소는 트렌드 키워드 수집부터 GPT를 활용한 마케팅 후킹 문장 생성, Notion 업로드 및 재시도 통계 기록까지 자동화하는 스크립트를 포함합니다.

## 의존성 설치

Python 3.10 이상에서 동작하며 다음 패키지가 필요합니다.

```bash
pip install openai python-dotenv notion-client pytrends snscrape
```

(또는 필요에 따라 `requirements.txt`를 만들어 사용해도 됩니다.)

## 환경 변수

모든 스크립트는 `.env` 파일이나 시스템 환경 변수로 설정값을 읽습니다. 주요 변수는 다음과 같습니다.

- `OPENAI_API_KEY` – GPT 호출에 사용되는 OpenAI API 키
- `NOTION_API_TOKEN` – Notion API 토큰
- `NOTION_DB_ID` – 키워드 업로드용 데이터베이스 ID
- `NOTION_HOOK_DB_ID` – 생성된 후킹을 저장할 데이터베이스 ID
- `NOTION_KPI_DB_ID` – 재시도 결과 KPI를 기록할 데이터베이스 ID
- 기타 각 스크립트에서 사용하는 경로 변수(아래 참고)

## 스크립트별 설명

### keyword_auto_pipeline.py

Google Trends와 Twitter 데이터를 수집하여 유망 키워드를 필터링합니다. 결과는 `KEYWORD_OUTPUT_PATH`(기본값 `data/keyword_output_with_cpc.json`)에 저장됩니다.

환경 변수
- `TOPIC_CHANNELS_PATH` – 토픽 목록 JSON 경로(기본값 `config/topic_channels.json`)
- `KEYWORD_OUTPUT_PATH` – 결과 저장 경로

실행 예:
```bash
python keyword_auto_pipeline.py
```

### hook_generator.py

필터링된 키워드를 입력 받아 GPT를 이용해 후킹 문장을 생성합니다. 성공한 결과는 `HOOK_OUTPUT_PATH`(기본값 `data/generated_hooks.json`)에 저장되며 실패한 항목은 `FAILED_HOOK_PATH`에 별도 기록됩니다.

환경 변수
- `OPENAI_API_KEY`
- `KEYWORD_OUTPUT_PATH` – 입력 파일 경로
- `HOOK_OUTPUT_PATH` – 생성 결과 저장 경로
- `FAILED_HOOK_PATH` – 실패 항목 저장 경로
- `API_DELAY` – 각 호출 사이의 지연 시간(초)

실행 예:
```bash
python hook_generator.py
```

### notion_hook_uploader.py

생성된 후킹 결과를 Notion 데이터베이스에 업로드합니다. 중복 확인 및 실패 항목 기록 기능을 제공합니다.

환경 변수
- `NOTION_API_TOKEN`
- `NOTION_HOOK_DB_ID`
- `HOOK_OUTPUT_PATH` – 입력 파일 경로
- `UPLOAD_DELAY` – 업로드 간 지연 시간(초)
- `FAILED_OUTPUT_PATH` – 업로드 실패 항목 저장 경로

실행 예:
```bash
python notion_hook_uploader.py
```

### retry_failed_uploads.py

업로드 실패 항목(`REPARSED_OUTPUT_PATH`)을 다시 Notion으로 전송합니다.

환경 변수
- `NOTION_API_TOKEN`
- `NOTION_HOOK_DB_ID`
- `REPARSED_OUTPUT_PATH` – 실패 항목 JSON 경로
- `RETRY_DELAY` – 재시도 간 지연 시간(초)

실행 예:
```bash
python retry_failed_uploads.py
```

### retry_dashboard_notifier.py

재시도 결과 요약을 읽어 KPI 데이터베이스(`NOTION_KPI_DB_ID`)에 기록합니다.

환경 변수
- `NOTION_API_TOKEN`
- `NOTION_KPI_DB_ID`
- `REPARSED_OUTPUT_PATH` – 재시도 결과 JSON 경로

실행 예:
```bash
python retry_dashboard_notifier.py
```

### scripts/notion_uploader.py

필터링된 키워드를 Notion에 업로드하는 초기 버전 스크립트입니다.

환경 변수
- `NOTION_API_TOKEN`
- `NOTION_DB_ID`
- `KEYWORD_OUTPUT_PATH`
- `UPLOADED_CACHE_PATH` – 업로드한 키워드 캐시 파일 경로
- `FAILED_UPLOADS_PATH` – 실패한 업로드 기록 경로
- `UPLOAD_DELAY`

### scripts/retry_failed_uploads.py

`FAILED_HOOK_PATH`에 기록된 실패 항목을 다시 업로드합니다. 설정 값은 `retry_failed_uploads.py`와 유사합니다.

## run_pipeline.py

`scripts` 디렉터리의 여러 스크립트를 순차적으로 실행하는 간단한 파이프라인 런처입니다. `PIPELINE_SEQUENCE`를 수정하여 실행 순서를 조정할 수 있습니다.

실행 예:
```bash
python run_pipeline.py
```

## GitHub Actions 사용법

`.github/workflows/daily-pipeline.yml.txt` 파일에는 매일 정해진 시간에 파이프라인을 실행하는 예제 워크플로가 들어 있습니다. 파일 이름을 `daily-pipeline.yml`로 변경하여 GitHub에 푸시하면 동작합니다. 워크플로는 다음 단계로 구성됩니다.

1. 저장소 체크아웃
2. Python 3.10 설정 후 의존성 설치
3. `scripts/run_pipeline.py` 실행
4. 실패 항목을 아티팩트로 업로드하고 실행 요약을 남김

실행에 필요한 비밀 값(`OPENAI_API_KEY`, `NOTION_API_TOKEN` 등)은 GitHub 리포지토리의 **Settings > Secrets** 메뉴에서 등록합니다.

