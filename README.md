--- README.md
# Auto Pipeline

이 저장소는 트렌딩 키워드 생성, OpenAI를 이용한 마케팅 훅 생성 및 Notion 업로드와  
다양한 플랫폼용 콘텐츠 변환 도구를 한 곳에 모아둔 프로젝트입니다.

## 주요 기능
- **키워드 자동화**  
  `keyword_auto_pipeline.py`로 트렌딩 키워드를 수집해 JSON 파일로 저장  
- **훅 생성**  
  `hook_generator.py`로 키워드를 기반한 마케팅 훅 생성  
- **Notion 업로드**  
  `notion_hook_uploader.py`로 생성된 훅을 Notion 데이터베이스에 업로드  
- **콘텐츠 변환**  
  `content_converter.py`의 `convert_content` 함수로 YouTube·Instagram·TikTok·Facebook·LinkedIn용 스크립트 생성

## 설치 및 초기 설정
1. Python 3.10 이상 설치  
2. 저장소 클론 후 의존성 설치:
   ```bash
   pip install -r requirements.txt
