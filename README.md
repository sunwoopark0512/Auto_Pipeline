# Auto Pipeline

이 저장소는 키워드 수집부터 Notion 업로드까지 자동화된 파이프라인을 제공합니다. 각 스크립트는 환경 변수를 통해 동작을 제어하며 `run_pipeline.py` 를 이용해 순차적으로 실행할 수 있습니다.

## 스크립트 설명

| 스크립트 | 역할 | 주요 환경 변수 |
|---|---|---|
| `keyword_auto_pipeline.py` | Google Trends와 Twitter에서 키워드를 수집하고 필터링하여 JSON으로 저장합니다. | `TOPIC_CHANNELS_PATH` – 토픽 설정 파일 경로 (기본 `config/topic_channels.json`)  
`KEYWORD_OUTPUT_PATH` – 결과 저장 경로 (기본 `data/keyword_output_with_cpc.json`) |
| `scripts/notion_uploader.py` | 수집된 키워드를 지정된 Notion DB에 업로드합니다. | `NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH` |
| `hook_generator.py` | 키워드를 입력 받아 GPT로 마케팅용 후킹 문장과 콘텐츠 초안을 생성합니다. | `OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY` |
| `notion_hook_uploader.py` | 생성된 후킹 문장을 Notion Hook DB에 업로드합니다. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY` |
| `retry_failed_uploads.py` | 업로드 실패 항목을 다시 시도합니다. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY` |
| `retry_dashboard_notifier.py` | 재시도 결과를 KPI 형식으로 Notion에 기록합니다. | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH` |
| `run_pipeline.py` | `scripts` 폴더에 위치한 여러 스크립트를 순서대로 실행합니다. | 없음 |

## 환경 변수 설정

모든 스크립트는 `.env` 파일을 통해 필요한 값을 읽어옵니다. 예시:

```bash
OPENAI_API_KEY=your-openai-key
NOTION_API_TOKEN=your-notion-token
NOTION_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_HOOK_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_KPI_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

필요한 값은 사용하는 스크립트에 따라 달라질 수 있습니다.

## 의존성 설치

프로젝트 루트에서 다음 명령어로 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 파이프라인 실행

모든 환경 변수를 설정한 뒤 `run_pipeline.py` 를 실행하면 정의된 순서대로 스크립트가 실행됩니다.

```bash
python run_pipeline.py
```

각 스크립트의 로그는 터미널에 출력되며 실패 여부도 확인할 수 있습니다.

## GitHub 워크플로 사용법

`.github/workflows/daily-pipeline.yml.txt` 파일에는 GitHub Actions 워크플로 정의가 포함되어 있습니다. 매일 지정된 시간에 자동 실행되며, 주요 단계는 다음과 같습니다.

1. 저장소 체크아웃 및 Python 설정
2. `requirements.txt` 설치
3. `scripts/run_pipeline.py` 실행
4. 실패한 항목을 아티팩트로 업로드하고 실행 요약을 작성

워크플로에서는 다음과 같은 시크릿을 설정해야 합니다:
`OPENAI_API_KEY`, `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `NOTION_KPI_DB_ID`, `SLACK_WEBHOOK_URL`.

필요 시 `workflow_dispatch` 이벤트를 통해 수동으로도 실행할 수 있습니다.
