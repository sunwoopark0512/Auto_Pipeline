# Auto Pipeline POC

This repository now includes minimal infrastructure components for a multi-language stack.

## Components

- **LLM Guardrail** using [Guardrails-ai](https://github.com/shreyashankar/gpt-guardrails). See `llm_monitor/guardrail_schema.yml` and `guardrail_wrapper.py` for a simple wrapper around OpenAI completions.
- **Cloudflare KV Exporter** in `edge/kv_exporter.js` exposes object counts for Prometheus.
- **Weights & Biases sweep** configuration (`ml/sweep.yaml`) and job (`ml/run_sweep.py`) demonstrate early stopping via Hyperband.
- **Pulumi Infrastructure** under `infra/pulumi` sets up a Render service, Cloudflare Worker and AWS DynamoDB table.

These snippets are provided as a minimal proof-of-concept and are not wired into the existing pipeline yet.
