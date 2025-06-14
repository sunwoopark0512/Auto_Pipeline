### 스크립트 배치 규칙
- **run_pipeline.py** 는 `PIPELINE_SEQUENCE`에 명시된 스크립트를 로드합니다.
- 각 스크립트 파일은 **루트 또는 `scripts/` 중 하나에만** 존재해야 하며, 두 위치에 중복되면 CI가 실패합니다.

### 개발 환경
- Python 3.12 사용을 권장합니다.
- 네트워크 제한이 있는 환경에서는 `pip config set global.index-url https://pypi.python.org/simple` 또는 사내 미러 주소를 설정해 주세요.
