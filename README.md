# Auto Pipeline

## Docker

```bash
# 최신 이미지 풀
docker pull ghcr.io/your-org/v-infinity:latest
# DRY-RUN 테스트
docker run --rm -e DRY_RUN=1 ghcr.io/your-org/v-infinity run_pipeline
```

GitHub Actions에서 push 되면 자동으로 latest 태그 업데이트됩니다.
