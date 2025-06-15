# Auto Pipeline

이 프로젝트는 여러 스크립트를 순차적으로 실행하여 Notion 데이터베이스에 정보를 업로드하는 파이프라인입니다.

## 설치

로컬 환경이나 GitHub Actions에서 모두 `requirements.txt` 파일을 이용해 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 사용법

환경 변수를 설정한 뒤 파이프라인을 실행합니다.

```bash
python run_pipeline.py
```

GitHub Actions 워크플로우에서도 동일한 `requirements.txt`를 사용해 의존성을 설치하도록 구성되어 있습니다.
