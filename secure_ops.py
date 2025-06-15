"""
Step-4: OIDC -> AWS Secrets Manager, ELK 로그, HPA, OpsGenie 알림
자동 설정 파일들을 생성합니다.
실행: python secure_ops.py
"""
from pathlib import Path
import textwrap, datetime, json

ROOT = Path(".")

def w(p, c):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(c).lstrip(), encoding="utf-8")
    print("\U0001f4dd", p)

# 1. GitHub Actions OIDC + AWS AssumeRole
w(ROOT / ".github/workflows/aws-secrets.yml", """
name: Sync Secrets

on:
  workflow_dispatch:
  schedule:
    - cron: '0 1 * * *'

permissions:
  id-token: write
  contents: read

env:
  AWS_REGION: ap-northeast-2

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubOIDC
          aws-region: ${{ env.AWS_REGION }}
      - name: Put OpenAI key
        run: |
          aws secretsmanager put-secret-value --secret-id /vinfinity/OPENAI_API_KEY --secret-string "$OPENAI_API_KEY"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
""")

# 2. k8s/elk-stack.yaml (Filebeat -> Logstash -> Elasticsearch)
w(ROOT / "k8s/elk-stack.yaml", """
apiVersion: v1
kind: Namespace
metadata: { name: logging }
---
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata: { name: vin-es, namespace: logging }
spec:
  version: 8.13.2
  nodeSets:
    - name: default
      count: 1
      config:
        node.store.allow_mmap: false
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata: { name: vin-kb, namespace: logging }
spec:
  version: 8.13.2
  count: 1
  elasticsearchRef: { name: vin-es }
""")

# 3. HorizontalPodAutoscaler 예시
w(ROOT / "k8s/hpa-api.yaml", """
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: { name: api-hpa }
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vinfinity-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
""")

# 4. OpsGenie 알림 Action
w(ROOT / ".github/workflows/alert.yml", """
name: OpsGenie Alert

on:
  workflow_run:
    workflows: ["CI Tests"]
    types: [failure]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send OpsGenie
        run: |
          curl -X POST https://api.opsgenie.com/v2/alerts \
            -H "Authorization: GenieKey $OG_KEY" \
            -H "Content-Type: application/json" \
            -d '{"message":"CI 실패","description":"${{ github.repository }}","priority":"P3"}'
        env:
          OG_KEY: ${{ secrets.OPSGENIE_KEY }}
""")

# 5. README 업데이트
readme = ROOT / "README.md"
if readme.exists() and "## 🛡 Security & Ops" not in readme.read_text():
    readme.write_text(readme.read_text() + textwrap.dedent("""
    ## 🛡 Security & Ops
    - **Secrets** : GitHub OIDC -> AWS Secrets Manager 자동 동기화
    - **Logging** : ECK (Elasticsearch + Kibana) 스택
    - **Autoscale** : HPA (CPU 70 % 이상 시 2 -> 10)
    - **Alerts** : CI 실패 -> OpsGenie P3 알림
    """), encoding="utf-8")

print("✅ Step-4 파일 생성 완료 — git add · commit · push 후 배포하면 보안·로그·HPA·알림까지 활성화됩니다.")
