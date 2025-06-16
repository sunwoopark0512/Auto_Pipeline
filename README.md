# Auto Pipeline

## AWS 비용 모니터링

`scripts/aws_cost_monitor.py` 스크립트는 AWS Cost Explorer API를 사용하여 현재 달의 비용을 조회합니다. 실행 전에 다음 환경 변수를 설정하거나 `.env` 파일에 추가하세요.

```bash
AWS_ACCESS_KEY_ID=YOUR_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET
AWS_SESSION_TOKEN=YOUR_TOKEN  # 선택 사항
AWS_REGION=us-east-1          # 기본값
```

설정 후 아래 명령어로 비용을 확인할 수 있습니다.

```bash
python scripts/aws_cost_monitor.py
```
