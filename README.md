# Auto Pipeline

This repository contains automation scripts and a small FastAPI service.

## Setup

```bash
make setup
```

## Lint

```bash
make lint
```

## Run locally

```bash
uvicorn api.main:app --reload
```

## Docker

```bash
docker build -t auto-pipeline .
docker run -p 8000:8000 -e API_KEY=changeme auto-pipeline
```
