# Auto Pipeline

이 레포지토리는 트렌드 키워드를 수집하고 GPT를 통해 마케팅 후킹 문장을 생성한 뒤 Notion 데이터베이스로 업로드하는 자동화 파이프라인을 제공합니다.

## 파이프라인 흐름
1. **키워드 수집** (`keyword_auto_pipeline.py`)
   - Google Trends와 Twitter에서 인기 키워드를 수집하고 필터링합니다.
   - 결과는 `KEYWORD_OUTPUT_PATH`에 JSON 형식으로 저장됩니다.
2. **후킹 생성** (`hook_generator.py`)
   - 수집한 키워드를 바탕으로 GPT API를 사용해 숏폼 후킹 문장, 블로그 초안, 영상 제목을 생성합니다.
   - 생성 결과는 `HOOK_OUTPUT_PATH`에 저장되며 실패한 항목은 별도 로그로 남습니다.
3. **Notion 업로드** (`notion_hook_uploader.py`)
   - 생성된 후킹 문장을 지정한 Notion 데이터베이스(`NOTION_HOOK_DB_ID`)에 업로드합니다.
4. **실패 재시도 및 KPI 기록** (`retry_failed_uploads.py`, `retry_dashboard_notifier.py`)
   - 업로드에 실패한 항목을 다시 시도하고 결과 요약을 KPI 데이터베이스(`NOTION_KPI_DB_ID`)에 저장합니다.

## 환경 변수
| 변수명 | 설명 |
| ------ | ---- |
| `OPENAI_API_KEY` | OpenAI API 호출에 사용되는 키 |
| `NOTION_API_TOKEN` | Notion API 접근 토큰 |
| `NOTION_HOOK_DB_ID` | 후킹 결과를 저장할 Notion DB ID |
| `NOTION_KPI_DB_ID` | 재시도 현황을 기록할 KPI DB ID |
| `KEYWORD_OUTPUT_PATH` | 키워드 수집 결과 파일 경로 |
| `HOOK_OUTPUT_PATH` | GPT가 생성한 후킹 결과 파일 경로 |
| `REPARSED_OUTPUT_PATH` | 실패 항목 재파싱 결과 저장 경로 |
| 기타 `API_DELAY`, `UPLOAD_DELAY`, `RETRY_DELAY` 등 세부 동작을 조절하는 변수들도 사용할 수 있습니다. |

환경 변수들은 `.env` 파일에 저장하거나 GitHub Actions의 Secrets로 설정해 사용할 수 있습니다.

## 로컬 실행 방법
1. Python 3.10 이상 환경을 준비하고 필요한 패키지를 설치합니다.
   ```bash
   pip install openai notion-client pytrends snscrape python-dotenv
   ```
2. 레포지토리 루트에 `.env` 파일을 생성하여 위의 환경 변수를 설정합니다.
3. 다음과 같이 각 스크립트를 순서대로 실행하거나 `run_pipeline.py`를 사용해 한 번에 실행할 수 있습니다.
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   python retry_failed_uploads.py
   python retry_dashboard_notifier.py
   ```

## GitHub Actions 사용법
- `.github/workflows/daily-pipeline.yml.txt` 워크플로우는 매일 정해진 시간에 파이프라인을 실행합니다.
- 레포지토리의 **Settings → Secrets**에 다음 값을 등록하면 자동으로 실행됩니다.
  - `OPENAI_API_KEY`
  - `NOTION_API_TOKEN`
  - `NOTION_HOOK_DB_ID`
  - `NOTION_KPI_DB_ID`
  - `SLACK_WEBHOOK_URL`(선택)
- 워크플로우 파일의 기본 실행 명령은 `python scripts/run_pipeline.py`입니다. 필요에 따라 경로와 스케줄을 수정해 사용할 수 있습니다.

