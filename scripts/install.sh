#!/usr/bin/env bash
# scripts/install.sh
# 자동 가상환경 + 의존 패키지 설치
set -e
PYTHON=${PYTHON:-python3.11}

$PYTHON -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
if [ ! -f requirements.txt ]; then
  echo "❌ requirements.txt not found"; exit 1
fi
pip install -r requirements.txt

echo "✅ install.sh complete.  Run 'source .venv/bin/activate' next."
