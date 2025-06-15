# v-Infinity Codex Admin Automation Module v1.0

본 모듈은 SaaS 운영 로그 기록을 자동화하기 위한 Codex Admin 엔진의 첫 버전입니다.

## 📦 기능
- Notion API 연동
- SaaS 운영 로그 표준화
- Codex CLI 기반 모듈 확장 가능

## 📂 파일 구조
- notion_client.py : Notion API Client
- ops_log_model.py : 표준 Log 모델 정의
- log_ops.py : CLI 실행 엔트리포인트
- .env.sample : 환경변수 예시

## ⚙️ 환경설정
- .env 파일 생성 후 Notion API Key 및 DB ID 입력
- Notion DB는 사전 생성 필요 (v-Infinity Ops Board 기반)

## 🚀 실행방법
```bash
python log_ops.py
향후 argparse 기반 CLI 확장 예정
```

---

✅ **이 상태 그대로 Codex → 새 프로젝트 → 바로 Import 가능**
