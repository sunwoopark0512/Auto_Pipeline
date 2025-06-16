# Auto Pipeline

자동화된 키워드 수집과 Notion 업로드를 위한 스크립트 모음입니다.

## 주요 환경 변수

| 이름 | 기본값 | 설명 |
| ---- | ------ | ---- |
| `TOPIC_CHANNELS_PATH` | `config/topic_channels.json` | 토픽 및 채널 설정 파일 경로 |
| `KEYWORD_OUTPUT_PATH` | `data/keyword_output_with_cpc.json` | 키워드 파이프라인 결과 저장 경로 |
| `MAX_WORKERS` | `10` | `keyword_auto_pipeline.py`에서 사용할 스레드 수 |

기타 Notion 업로드 및 GPT 호출과 관련된 토큰은 GitHub Secrets를 통해 전달됩니다.
