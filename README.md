# Auto Pipeline

본 프로젝트는 Notion API와 OpenAI를 활용한 자동화 파이프라인 예제입니다.

## 환경 변수 설정
1. `.env.example` 파일을 참고하여 `.env` 파일을 만듭니다.
   ```bash
   cp .env.example .env
   ```
2. `.env` 파일의 각 값에 실제 토큰과 설정을 채워 넣습니다.

프로젝트의 스크립트들은 실행 시 `.env` 파일의 환경 변수를 로드합니다.
