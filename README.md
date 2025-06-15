# Auto Pipeline

Auto Pipeline은 인기 키워드를 수집하여 마케팅에 활용할 후킹 문장을 생성하고, 결과를 노션 데이터베이스에 업로드하는 작업을 자동화하기 위한 파이프라인입니다. Google Trends와 Twitter 데이터를 이용해 키워드를 수집하고 OpenAI API를 사용하여 콘텐츠 아이디어를 만들어 줍니다.

## 주요 스크립트

|스크립트|설명|
|---|---|
|`keyword_auto_pipeline.py`|Google Trends와 Twitter에서 데이터를 수집해 필터링된 키워드를 JSON 파일(`data/keyword_output_with_cpc.json`)로 저장합니다.|
|`hook_generator.py`|수집된 키워드를 기반으로 OpenAI API를 호출해 후킹 문장과 블로그 초안, 영상 제목을 생성합니다. 결과는 `data/generated_hooks.json`에 기록됩니다.|
|`notion_hook_uploader.py`|생성된 후킹 데이터를 지정된 노션 데이터베이스로 업로드합니다.|
|`retry_failed_uploads.py`|업로드 실패 항목을 다시 시도합니다.|
|`retry_dashboard_notifier.py`|재시도 결과를 요약해 KPI용 노션 데이터베이스에 기록합니다.|
|`run_pipeline.py`|위 과정을 한 번에 실행하기 위한 간단한 래퍼 스크립트입니다.|

## 실행 순서 예시

1. `.env` 파일을 작성해 필요한 환경 변수를 설정합니다.
2. 키워드 수집: `python keyword_auto_pipeline.py`
3. 후킹 문장 생성: `python hook_generator.py`
4. 노션 업로드: `python notion_hook_uploader.py`
5. 실패 항목 재업로드 및 KPI 업데이트(필요 시):
   ```bash
   python retry_failed_uploads.py
   python retry_dashboard_notifier.py
   ```
6. 모든 단계를 한 번에 실행하려면 `python run_pipeline.py`를 사용할 수 있습니다.

## .env 예시

```
OPENAI_API_KEY=sk-xxxx
NOTION_API_TOKEN=secret_token
NOTION_HOOK_DB_ID=xxxxxxxxxxxxxxxxx
NOTION_DB_ID=xxxxxxxxxxxxxxxxx
NOTION_KPI_DB_ID=xxxxxxxxxxxxxxxxx
KEYWORD_OUTPUT_PATH=data/keyword_output_with_cpc.json
HOOK_OUTPUT_PATH=data/generated_hooks.json
FAILED_HOOK_PATH=logs/failed_hooks.json
FAILED_UPLOADS_PATH=logs/failed_uploads.json
UPLOADED_CACHE_PATH=data/uploaded_keywords_cache.json
REPARSED_OUTPUT_PATH=logs/failed_keywords_reparsed.json
UPLOAD_DELAY=0.5
RETRY_DELAY=0.5
API_DELAY=1.0
TOPIC_CHANNELS_PATH=config/topic_channels.json
```

> **주의:** 실제 토큰 값은 절대 커밋하지 마세요. `.gitignore`에 `.env`가 포함되어 있습니다.

## GitHub Actions 사용 시 주의사항

- 워크플로 파일은 `.github/workflows/daily-pipeline.yml.txt`로 제공됩니다. GitHub Actions에서 사용하려면 확장자를 `.yml`로 변경해야 합니다.
- 스케줄 설정은 매일 오전 9시(KST)에 실행되도록 되어 있으며, 필요한 경우 수정할 수 있습니다.
- OpenAI 및 Notion 관련 토큰은 저장소의 **Secrets**에 `OPENAI_API_KEY`, `NOTION_API_TOKEN`, `NOTION_HOOK_DB_ID`, `NOTION_KPI_DB_ID` 등으로 등록해야 합니다.
- 워크플로가 실행되면 로그와 실패한 항목이 `logs/failed_keywords_reparsed.json` 파일로 아티팩트 업로드 됩니다.

