# Auto Pipeline

이 저장소는 키워드 트렌드 수집부터 콘텐츠 후킹 문장 생성,
Notion 업로드 및 실패 항목 재시도까지의 과정을 자동화합니다.

## 파이프라인 개요
1. **키워드 수집** (`keyword_auto_pipeline.py`)
   - Google Trends와 Twitter 데이터를 기반으로 주제별 키워드 후보를 수집하고 필터링하여 `KEYWORD_OUTPUT_PATH` 위치에 JSON으로 저장합니다.
2. **Hook 생성** (`hook_generator.py`)
   - 앞 단계에서 저장된 키워드를 읽어 OpenAI API를 통해 숏폼 후킹 문장, 블로그 초안, 유튜브 제목 등을 생성하고 `HOOK_OUTPUT_PATH` 파일에 기록합니다.
3. **Notion 업로드** (`notion_hook_uploader.py`)
   - 생성된 Hook 데이터를 지정된 Notion 데이터베이스(`NOTION_HOOK_DB_ID`)에 업로드합니다. 실패한 항목은 별도의 로그로 남깁니다.
4. **재시도** (`retry_failed_uploads.py`)
   - 업로드 실패 항목을 `REPARSED_OUTPUT_PATH`에서 불러와 다시 Notion으로 전송하고 결과를 요약하여 KPI DB(`NOTION_KPI_DB_ID`)에 기록합니다.

## 환경 변수
다음 변수들은 `.env` 또는 실행 환경에서 설정해야 합니다.

| 변수명 | 설명 | 기본값 |
| ------ | ---- | ------ |
| `OPENAI_API_KEY` | OpenAI API 키 | - |
| `NOTION_API_TOKEN` | Notion 통합 토큰 | - |
| `NOTION_HOOK_DB_ID` | 생성된 Hook를 저장할 Notion DB ID | - |
| `NOTION_KPI_DB_ID` | 재시도 결과를 저장할 KPI DB ID | - |
| `KEYWORD_OUTPUT_PATH` | 키워드 JSON 결과 경로 | `data/keyword_output_with_cpc.json` |
| `HOOK_OUTPUT_PATH` | Hook JSON 결과 경로 | `data/generated_hooks.json` |
| `REPARSED_OUTPUT_PATH` | 재시도용 실패 데이터 경로 | `logs/failed_keywords_reparsed.json` |

## 로컬 실행 방법
1. 필요한 파이썬 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt  # 필요 시
   ```
2. `.env` 파일에 위 환경 변수를 설정합니다.
3. 다음 순서대로 스크립트를 실행합니다.
   ```bash
   python keyword_auto_pipeline.py
   python hook_generator.py
   python notion_hook_uploader.py
   python retry_failed_uploads.py  # 필요 시 실패 항목 재업로드
   ```

## GitHub Actions 사용
`.github/workflows/daily-pipeline.yml.txt` 워크플로를 통해 매일 자동으로 파이프라인을 실행할 수 있습니다. 저장소의 `Secrets`에 위 환경 변수들을 등록하면 스케줄(또는 수동 실행)로 동작합니다.

