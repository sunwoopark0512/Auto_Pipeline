FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir ddtrace requests pytest
CMD ["python", "run_pipeline.py"]
