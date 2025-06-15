# Makefile for staging preview automation
REPO ?= $(shell gh repo view --json nameWithOwner -q .nameWithOwner)
BRANCH ?= main
ARTIFACT_DIR ?= staging_artifacts
ENV_FILE ?= .env.staging.local
COMPOSE_FILE ?= docker-compose.staging.yml

.PHONY: preview-staging cleanup-staging

# 1) Download latest artifacts and launch compose
preview-staging:
@echo "🔽 Pulling latest workflow run artifacts from $(BRANCH)..."
gh run download --repo $(REPO) --pattern "$(COMPOSE_FILE)" --dir $(ARTIFACT_DIR) --branch $(BRANCH) --latest
gh run download --repo $(REPO) --pattern "newsletter-preview*" --dir $(ARTIFACT_DIR) --branch $(BRANCH) --latest || true
@if [ ! -f $(ENV_FILE) ]; then \
echo "⚠️  $(ENV_FILE) not found. Creating template..."; \
echo "OPENAI_API_KEY=\nNOTION_API_TOKEN=\nTWITTER_BEARER_TOKEN=\nAPI_KEYS=staging123" > $(ENV_FILE); \
echo "→ Please fill in secrets inside $(ENV_FILE)"; exit 1; \
fi
@echo "⏩ Starting Docker Compose..."
docker compose -f $(ARTIFACT_DIR)/$(COMPOSE_FILE) --env-file $(ENV_FILE) up -d
@echo "⏳ Waiting 10s for services..."
sleep 10
@echo "📡 Probing API..."
curl -H "X-API-KEY:staging123" -s http://localhost:8000/v1/keywords?limit=1 | jq .
@if [ -f $(ARTIFACT_DIR)/newsletter-preview/newsletter.html ]; then \
echo "🌐 Opening newsletter preview..."; \
python - <<'PY' \
import webbrowser, os
webbrowser.open(os.path.join("$(ARTIFACT_DIR)", "newsletter-preview", "newsletter.html"))
PY
fi
@echo "✅ Preview ready at http://localhost:8000"

# 2) Cleanup
cleanup-staging:
docker compose -f $(ARTIFACT_DIR)/$(COMPOSE_FILE) down || true
rm -rf $(ARTIFACT_DIR)
@echo "🧹 Staging environment cleaned."
