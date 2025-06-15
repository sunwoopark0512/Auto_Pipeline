# ----------------- Quality & CI targets -----------------
PY       ?= python
PIP      ?= pip

.PHONY: lint test cov-html ci docker-build docker-run clean

# 1) 코드 품질 점검
lint:
    pre-commit run --all-files

# 2) 단위 테스트
test:
    pytest -q

# 3) 커버리지 HTML
cov-html:
    pytest --cov=./ --cov-report=html
    @echo "🔍 opening htmlcov/index.html"
    $(PY) - <<'PY'
import webbrowser, pathlib, sys
webbrowser.open(pathlib.Path("htmlcov/index.html").absolute().as_uri())
PY

# 4) 로컬 CI 풀 사이클 (lint+test+codecov+docker 빌드)
ci: lint test
    @echo "📈 Upload to Codecov (local token needed)"
    @if [ -n "$$CODECOV_TOKEN" ]; then \
        pytest --cov=./ --cov-report=xml -q && \
        bash <(curl -s https://codecov.io/bash) -f coverage.xml; \
    else \
        echo "CODECOV_TOKEN not set; skipping upload."; \
    fi
    make docker-build

# 5) Docker 빌드 & 실행
docker-build:
    docker build -t autopipeline:dev .

docker-run: docker-build
    docker run -d --name autopipe_dev -p 8000:8000 \
        -e "API_KEYS=local123" autopipeline:dev
    @echo "API running at http://localhost:8000 (X-API-KEY: local123)"

# 6) 정리
clean:
    @echo "🧹 Cleaning caches..."
    rm -rf .pytest_cache .mypy_cache htmlcov
    find . -type d -name '__pycache__' -exec rm -rf {} +
