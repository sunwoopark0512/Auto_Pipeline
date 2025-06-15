# build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip wheel && pip wheel -r requirements.txt -w /tmp/wheels

# runtime stage
FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/your-org/your-repo"
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /tmp/wheels /tmp/wheels
RUN pip install --no-index --find-links=/tmp/wheels /tmp/wheels/* && rm -rf /tmp/wheels
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
