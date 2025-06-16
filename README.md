# Auto_Pipeline

이 저장소는 키워드 트렌드를 수집하고, OpenAI를 통해 마케팅용 후킹 문장을 생성하며, Notion에 업로드하는 자동 파이프라인 스크립트를 제공합니다.

## 스크립트 개요

| 스크립트 | 설명 | 주요 환경 변수 |
|----------|------|----------------|
| `keyword_auto_pipeline.py` | 구글 트렌드와 트위터 데이터를 수집하여 필터링된 키워드를 생성합니다. 결과는 `KEYWORD_OUTPUT_PATH` 위치에 JSON으로 저장됩니다. | `TOPIC_CHANNELS_PATH`, `KEYWORD_OUTPUT_PATH` |
| `hook_generator.py` | 필터링된 키워드를 기반으로 OpenAI API를 호출하여 후킹 문장과 블로그 초안 등을 생성합니다. | `OPENAI_API_KEY`, `KEYWORD_OUTPUT_PATH`, `HOOK_OUTPUT_PATH`, `FAILED_HOOK_PATH`, `API_DELAY` |
| `notion_hook_uploader.py` | 생성된 후킹 데이터를 Notion 데이터베이스에 업로드합니다. 실패한 항목은 `data/upload_failed_hooks.json`에 기록됩니다. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `HOOK_OUTPUT_PATH`, `UPLOAD_DELAY` |
| `retry_failed_uploads.py` | 업로드에 실패한 키워드를 다시 Notion으로 업로드합니다. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `REPARSED_OUTPUT_PATH`, `RETRY_DELAY` |
| `retry_dashboard_notifier.py` | 재시도 결과 요약을 읽어 KPI를 계산하고 별도의 Notion DB에 기록합니다. | `NOTION_API_TOKEN`, `NOTION_KPI_DB_ID`, `REPARSED_OUTPUT_PATH` |
| `scripts/notion_uploader.py` | `keyword_auto_pipeline.py`가 생성한 키워드를 다른 Notion DB에 업로드하는 보조 스크립트입니다. | `NOTION_API_TOKEN`, `NOTION_DB_ID`, `KEYWORD_OUTPUT_PATH`, `UPLOAD_DELAY`, `UPLOADED_CACHE_PATH`, `FAILED_UPLOADS_PATH` |
| `scripts/retry_failed_uploads.py` | `hook_generator.py` 실행 중 실패한 후킹 데이터를 다시 업로드합니다. | `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `FAILED_HOOK_PATH`, `RETRY_DELAY` |
| `run_pipeline.py` | 여러 스크립트를 순차적으로 실행하는 간단한 실행기입니다. `PIPELINE_SEQUENCE` 변수에 실행 순서가 정의되어 있습니다. | - |

## 요구 사항 설치

프로젝트의 Python 의존성은 `requirements.txt` 파일에 정의되어 있습니다. 다음 명령어로 필요한 패키지를 설치합니다.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 파이프라인 실행

모든 환경 변수를 `.env` 파일에 설정한 뒤 아래 명령어로 전체 파이프라인을 실행할 수 있습니다.

```bash
python run_pipeline.py
```

`run_pipeline.py`는 `PIPELINE_SEQUENCE`에 명시된 스크립트를 차례로 호출합니다. 기본적으로 `scripts` 디렉터리에서 해당 파일을 찾으므로 경로나 파일명이 변경되었다면 `PIPELINE_SEQUENCE`를 수정해야 합니다.

## GitHub Actions 사용하기

`.github/workflows/daily-pipeline.yml.txt` 파일에는 매일 정해진 시각에 파이프라인을 실행하도록 설정된 GitHub Actions 워크플로 예제가 포함되어 있습니다. 필요한 비밀 값(예: `OPENAI_API_KEY`, `NOTION_API_TOKEN` 등)을 리포지터리의 Secrets에 등록한 후 파일 확장자를 `.yml`로 변경하면 워크플로가 활성화됩니다.

워크플로는 다음 단계를 수행합니다.

1. 저장소 체크아웃
2. Python 3.10 설치
3. `requirements.txt`로 의존성 설치
4. `scripts/run_pipeline.py` 실행 (필요 시 경로 수정)
5. 실패 항목 JSON을 아티팩트로 업로드
6. 실행 결과를 `workflow summary`에 기록

이 워크플로를 통해 서버를 따로 두지 않고도 주기적으로 파이프라인을 자동 실행할 수 있습니다.
