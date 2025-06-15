# ---------- 글로벌 변수 ----------
PYTHON := python3
TAG ?= dev
PORT ?= 8000
API_KEY ?= local
REGISTRY ?= ghcr.io
REPO ?= autopipeline

.PHONY: lint test cov-html ci docker-build docker-run \
        publish-docker publish-latest docker-stop clean-images clean

lint:
	$(PYTHON) -m py_compile $(shell git ls-files '*.py')

# run basic unittest discovery if present
test:
	$(PYTHON) -m unittest discover -v || true

cov-html:
	@echo "No coverage setup"

ci: lint test

# ---------- Docker 관련 타깃 ----------

# 1) Build image
#    e.g. make docker-build TAG=v0.1

docker-build:
	docker build \
	-t $(REGISTRY)/$(REPO):$(TAG) \
	--build-arg API_KEY=$(API_KEY) \
	.

# 2) Run container

docker-run: docker-build
	docker run -d --name autopipe_$(TAG) \
	-p $(PORT):8000 \
	-e API_KEY=$(API_KEY) \
	$(REGISTRY)/$(REPO):$(TAG)
	@echo "\ud83c\udf10 API \u2192 http://localhost:$(PORT)  (X-API-KEY: $(API_KEY))"

# 3) Push image to registry

publish-docker:
docker push $(REGISTRY)/$(REPO):$(TAG)

# ---------- 추가 Docker 유틸 타깃 ----------------

# 1) \ub85c\uceec \ucee4\ud2f0\ub124\uc774\ubc84 \uc911\ub2e8

docker-stop:
	- docker stop autopipe_$(TAG) 2>/dev/null || true
	@echo "\ud83d\udd1d Stopped container autopipe_$(TAG)"

# 2) \uae30\uc874 publish + latest \ud0dc\uadf8 \ucd94\uac00

publish-latest: publish-docker
	@echo "\ud83d\udd04 Tagging image as latest..."
	docker tag $(REGISTRY)/$(REPO):$(TAG) $(REGISTRY)/$(REPO):latest
	docker push $(REGISTRY)/$(REPO):latest
	@echo "\u2705 $(REGISTRY)/$(REPO):latest pushed."

# 3) \ub85c\uceec \uc774\ubbf8\uc9c0\xb7\uce90\uc2dc \uc815\ub9ac

clean-images:
	@echo "\ud83e\uddf9 Removing local autopipeline images & dangling layers"
	docker rm -f $(shell docker ps -aqf "name=autopipe_") 2>/dev/null || true
	docker images "autopipeline:*" -q | xargs -r docker rmi -f
	docker image prune -f

clean:
	rm -rf __pycache__ */__pycache__
