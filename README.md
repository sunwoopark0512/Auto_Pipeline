# Auto Pipeline

이 프로젝트는 키워드 수집부터 콘텐츠 후킹 생성, Notion 업로드까지 자동화된 파이프라인을 제공합니다. 실패한 업로드는 재시도하여 Notion KPI 대시보드에 결과를 기록합니다.

## 파이프라인 흐름
1. **키워드 수집**: `keyword_auto_pipeline.py`가 Google Trends와 Twitter 데이터를 기반으로 키워드를 필터링하여 `KEYWORD_OUTPUT_PATH`에 저장합니다.
2. **후킹 생성**: `hook_generator.py`가 필터링된 키워드로부터 GPT를 활용해 후킹 문장과 블로그/영상 초안을 생성하여 `HOOK_OUTPUT_PATH`에 기록합니다.
3. **Notion 업로드**: `notion_hook_uploader.py`가 생성된 후킹 결과를 Notion DB(`NOTION_HOOK_DB_ID`)에 업로드합니다.
4. **실패 재시도**: `retry_failed_uploads.py`가 업로드 실패 항목(`REPARSED_OUTPUT_PATH`)을 다시 시도하고, `retry_dashboard_notifier.py`가 KPI DB(`NOTION_KPI_DB_ID`)에 성공률을 기록합니다.

## 환경 변수
| 변수명 | 설명 |
| ------ | ---- |
| `OPENAI_API_KEY` | OpenAI API 키 |
| `NOTION_API_TOKEN` | Notion API 토큰 |
| `NOTION_HOOK_DB_ID` | 후킹 결과를 저장할 Notion 데이터베이스 ID |
| `NOTION_KPI_DB_ID` | 재시도 결과 KPI를 기록할 Notion 데이터베이스 ID |
| `KEYWORD_OUTPUT_PATH` | 키워드 JSON 저장 경로 (기본: `data/keyword_output_with_cpc.json`) |
| `HOOK_OUTPUT_PATH` | 후킹 결과 JSON 저장 경로 (기본: `data/generated_hooks.json`) |
| `REPARSED_OUTPUT_PATH` | 업로드 실패 항목 JSON 경로 (기본: `logs/failed_keywords_reparsed.json`) |

## 로컬 실행
1. Python 3.10 환경을 준비하고 필요한 패키지를 설치합니다.
2. 위 환경 변수를 포함한 `.env` 파일을 작성합니다.
3. 순서대로 다음 스크립트를 실행합니다.
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   python retry_failed_uploads.py  # 실패 항목이 있는 경우
   python retry_dashboard_notifier.py
   ```

## GitHub Actions 사용
`.github/workflows/daily-pipeline.yml.txt` 워크플로를 통해 매일 자동으로 파이프라인을 실행할 수 있습니다. 리포지토리의 `Secrets`에 위 환경 변수를 등록하면 됩니다.

