# Makefile for Auto_Pipeline

# ---------------- 글로벌 변수 (필요 시 CLI에서 덮어쓰기) --------------
PY        ?= python
TFLAGS    ?= -q                   # pytest 플래그
TAG       ?= dev                  # Docker 이미지 태그
API_KEY   ?= local123             # FastAPI 테스트 키
PORT      ?= 8000

.PHONY: lint test cov-html ci docker-build docker-run clean

# ------------ 테스트 / 린트 -------------

lint:
	pylint *.py scripts/*.py || true

test:
	pytest $(TFLAGS)

cov-html:
	pytest --cov=./ --cov-report=html

ci: lint test

# ------------ Docker 빌드 / 실행 -------------

dker?=@echo "⚠️  'make dker' is a shortcut: use TAB-completion"; false

docker-build:
	docker build -t autopipeline:$(TAG) .

docker-run: docker-build
	docker run -d --rm --name autopipe_$(TAG) -p $(PORT):8000 -e "API_KEYS=$(API_KEY)" autopipeline:$(TAG)
	@echo "🌐 API → http://localhost:$(PORT)  (X-API-KEY: $(API_KEY))"

clean:
	rm -rf __pycache__ */__pycache__
