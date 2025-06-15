# ---------- 글로벌 변수 ----------
PY        ?= python
TFLAGS    ?= -q
TAG       ?= dev
REGISTRY  ?= ghcr.io
REPO      ?= $(shell gh repo view --json nameWithOwner -q .nameWithOwner)
PLATFORMS ?= linux/amd64,linux/arm64
API_KEY   ?= local123
PORT      ?= 8000

.PHONY: lint test cov-html ci docker-build docker-run publish-docker clean

lint:
	$(PY) -m flake8

test:
	$(PY) -m pytest $(TFLAGS)

cov-html:
	$(PY) -m pytest --cov --cov-report html $(TFLAGS)

ci: lint test

docker-build:
	docker build -t autopipeline:$(TAG) .

docker-run: docker-build
	docker run -d --rm --name autopipe_$(TAG) -p $(PORT):8000 -e "API_KEYS=$(API_KEY)" autopipeline:$(TAG)
	@echo "🌐 API → http://localhost:$(PORT)  (X-API-KEY: $(API_KEY))"

# -------------- Docker Publish (multi-arch) ----------------
publish-docker:
	@echo "🔑 Logging in to $(REGISTRY) ..."
	docker login $(REGISTRY) -u $(shell echo $$DOCKER_USER) -p $(shell echo $$DOCKER_TOKEN)
	@echo "🛠  Building & pushing autopipeline:$(TAG) for $(PLATFORMS)"
	docker buildx build . \
	  --platform $(PLATFORMS) \
	  --tag $(REGISTRY)/$(REPO):$(TAG) \
	  --push \
	  --build-arg BUILDKIT_INLINE_CACHE=1
	@echo "✅ Image pushed: $(REGISTRY)/$(REPO):$(TAG)"

clean:
	docker rm -f autopipe_$(TAG) || true
	docker rmi autopipeline:$(TAG) || true

