# Auto Pipeline

이 저장소는 인기 키워드 수집부터 GPT 후킹 문장 생성, 노션 업로드까지 자동화된 파이프라인을 제공합니다.

## 사용 방법
1. 필요한 Python 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```
2. 실행에 필요한 환경 변수를 `.env` 파일에 설정합니다(아래 표 참고).
3. 파이프라인을 실행합니다.
   ```bash
   python run_pipeline.py
   ```

## 주요 스크립트
- `keyword_auto_pipeline.py`: Google Trends와 Twitter에서 데이터를 수집해 필터링된 키워드를 생성합니다.
- `hook_generator.py`: OpenAI API를 이용해 각 키워드에 대한 후킹 문장을 생성합니다.
- `notion_hook_uploader.py`: 생성된 후킹 문장을 Notion 데이터베이스에 업로드합니다.
- `retry_failed_uploads.py`: 업로드 실패 항목을 다시 시도합니다.
- `retry_dashboard_notifier.py`: 재시도 결과를 KPI 대시보드에 전송합니다.

## 환경 변수
| 이름 | 설명 | 기본값 |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API 키 | - |
| `API_DELAY` | GPT 호출 간 대기 시간(초) | `1.0` |
| `KEYWORD_OUTPUT_PATH` | 키워드 결과 JSON 경로 | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | 생성된 후킹 결과 JSON 경로 | `data/generated_hooks.json` |
| `FAILED_HOOK_PATH` | GPT 생성 실패 항목 저장 경로 | `logs/failed_hooks.json` |
| `NOTION_API_TOKEN` | Notion 통합 토큰 | - |
| `NOTION_HOOK_DB_ID` | 후킹 데이터를 저장할 Notion DB ID | - |
| `NOTION_KPI_DB_ID` | KPI 정보를 저장할 Notion DB ID | - |
| `REPARSED_OUTPUT_PATH` | 재파싱된 실패 항목 파일 경로 | `logs/failed_keywords_reparsed.json` |
| `RETRY_DELAY` | 재시도 간 대기 시간(초) | `0.5` |
| `UPLOAD_DELAY` | 업로드 간 대기 시간(초) | `0.5` |
| `NOTION_DB_ID` | 키워드 데이터를 저장할 Notion DB ID | - |
| `UPLOADED_CACHE_PATH` | 이미 업로드된 키워드 캐시 경로 | `data/uploaded_keywords_cache.json` |
| `FAILED_UPLOADS_PATH` | 업로드 실패 항목 저장 경로 | `logs/failed_uploads.json` |
| `TOPIC_CHANNELS_PATH` | 주제 채널 목록 JSON 경로 | `config/topic_channels.json` |

모든 스크립트는 환경 변수 설정에 의존하므로 실행 전 `.env` 파일을 적절히 구성해야 합니다.

