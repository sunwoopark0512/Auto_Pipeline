# Auto Pipeline

This repository contains scripts to generate marketing hooks and upload them to Notion.

## Running with Docker

```bash
docker run --rm \
  -e OPENAI_API_KEY=xxx \
  -e NOTION_API_TOKEN=xxx \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=https://otel.example.com \
  ghcr.io/your-org/auto-pipeline:latest \
  python scripts/run_pipeline.py
```

## OpenTelemetry

Tracing data is exported via OTLP. Set `OTEL_EXPORTER_OTLP_ENDPOINT` to your collector endpoint. When `DRY_RUN=1` is set, spans will include an attribute `dry=true`.

See [Smoke test](https://example.com/smoke-test) for validating pushed images.
