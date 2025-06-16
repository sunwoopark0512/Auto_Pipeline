#!/bin/bash
METRICS_URL=${METRICS_URL:-http://localhost:8000/metrics}
if ! curl -sf "$METRICS_URL" > /dev/null; then
  if [ -n "$SLACK_WEBHOOK" ]; then
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Auto Pipeline health check failed"}' "$SLACK_WEBHOOK"
  fi
  exit 1
fi
