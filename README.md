# Auto Pipeline

이 프로젝트는 키워드 트렌드 수집부터 마케팅용 Hook 생성, Notion 업로드까지 자동화한 스크립트 모음입니다. GitHub Actions를 이용해 매일 파이프라인을 실행하거나 로컬에서 수동으로 실행할 수 있습니다.

## 파이프라인 개요
1. **키워드 수집**: `keyword_auto_pipeline.py`가 Google Trends와 Twitter에서 데이터를 모아 기준에 맞게 필터링합니다.
2. **Hook 생성**: `hook_generator.py`가 수집한 키워드를 기반으로 OpenAI를 호출해 후킹 문장과 블로그 초안, 영상 제목 예시를 만듭니다.
3. **Notion 업로드**: `notion_hook_uploader.py`가 생성된 Hook을 지정한 Notion 데이터베이스에 저장합니다.
4. **실패 재시도**: 업로드에 실패한 항목은 `retry_failed_uploads.py`와 `retry_dashboard_notifier.py`에서 다시 시도하고 결과를 요약합니다.

## 환경 변수
파이프라인 실행에 필요한 주요 환경 변수는 다음과 같습니다.

| 변수 | 용도 | 기본값 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 호출에 사용 | - |
| `NOTION_API_TOKEN` | Notion 통신을 위한 토큰 | - |
| `NOTION_HOOK_DB_ID` | Hook 저장용 데이터베이스 ID | - |
| `NOTION_KPI_DB_ID` | 재시도 통계 저장용 데이터베이스 ID | - |
| `NOTION_DB_ID` | 키워드 업로드용 데이터베이스 ID (옵션) | - |
| `KEYWORD_OUTPUT_PATH` | 수집된 키워드 JSON 경로 | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | 생성된 Hook JSON 경로 | `data/generated_hooks.json` |
| `FAILED_HOOK_PATH` | Hook 생성 실패 로그 경로 | `logs/failed_hooks.json` |
| `REPARSED_OUTPUT_PATH` | 실패 항목 재파싱 결과 경로 | `logs/failed_keywords_reparsed.json` |
| `TOPIC_CHANNELS_PATH` | 주제 설정 파일 경로 | `config/topic_channels.json` |
| `UPLOADED_CACHE_PATH` | 이미 업로드된 키워드 캐시 경로 | `data/uploaded_keywords_cache.json` |
| `FAILED_UPLOADS_PATH` | 키워드 업로드 실패 로그 경로 | `logs/failed_uploads.json` |
| `UPLOAD_DELAY` | Notion 업로드 간 대기 시간 | `0.5` |
| `RETRY_DELAY` | 재시도 간 대기 시간 | `0.5` |
| `API_DELAY` | OpenAI API 호출 간 대기 시간 | `1.0` |

## 로컬 실행 방법
1. 위 환경 변수를 `.env` 파일에 설정합니다.
2. 필요한 패키지(`openai`, `notion-client`, `python-dotenv`, `pytrends`, `snscrape` 등)를 설치합니다.
3. `python run_pipeline.py` 명령으로 전체 파이프라인을 실행하거나 각 스크립트를 개별적으로 실행할 수 있습니다.

```bash
pip install openai notion-client python-dotenv pytrends snscrape
python run_pipeline.py
```

실패 항목이 있을 경우 `retry_failed_uploads.py`를 실행해 재업로드를 시도할 수 있습니다.

## GitHub Actions 사용법
자동 실행을 원한다면 GitHub 저장소의 [`daily-pipeline.yml.txt`](.github/workflows/daily-pipeline.yml.txt) 워크플로를 활용합니다. 매일 정해진 시각에 파이프라인을 실행하며, 필요한 비밀 값은 GitHub Secrets에 등록해야 합니다.

```yaml
# 주요 환경 변수 예시 (Secrets)
OPENAI_API_KEY
NOTION_API_TOKEN
NOTION_HOOK_DB_ID
NOTION_KPI_DB_ID
```

워크플로는 실행 후 실패한 항목을 아티팩트로 저장하고, 요약 정보를 Workflow Summary에 남깁니다.
